# 2.Scheduler调度机制解析

## 一、整体目标与核心结论

### 🎯 Day 2 目标

理解 ArduPilot 中：

* `loop()` 到底在哪里
* 飞控任务是如何**按不同频率运行**
* 为什么飞控不会因为 delay / 阻塞而“失联”

---

### ✅ 核心结论

> **ArduPilot 通过 AP_Scheduler 统一调度任务（主路径），
> 并额外通过 delay callback 提供“兜底心跳”，保证系统不失联。**

---

## 二、程序主调用链（从 main 到调度器）

### 1️⃣ 程序入口

程序从 `main()` 启动，随后进入 HAL 层运行循环：

```text
main
 └─ HAL_Linux::run()
```

---

### 2️⃣ AP_Vehicle::loop（核心循环）

在 `HAL_Linux::run()` 中，会调用：

```cpp
void AP_Vehicle::loop()
```

关键点：

* `AP_Vehicle::loop()` 被声明为 `final`  `void loop() override final;`
* final 修饰的函数 **子类（如 Copter）不能重写**
* 所有飞行器共用这一套调度骨架

源码片段（简化）：

```cpp
void AP_Vehicle::loop()
{
#if AP_SCHEDULER_ENABLED
    scheduler.loop();
    G_Dt = scheduler.get_loop_period_s();
#else
    hal.scheduler->delay(1);
    G_Dt = 0.001;
#endif
...
...
    run(time_available);
}
```

---

### 3️⃣ 进入调度器：AP_Scheduler

```text
AP_Vehicle::loop
 └─ scheduler.loop()
     └─ scheduler.run()
```

`scheduler.run()` 会遍历并执行：

* `_vehicle_tasks`（机型相关任务，如 Copter）
* `_common_tasks`（通用任务）

并且检查当前任务是否超时，超时过多则会降低定时任务频率以提升每个周期运行时间，来处理延时的任务
---

## 三、Scheduler 的任务模型（主调度路径）

### 1️⃣ `_common_tasks`（通用任务）

定义位置：

```text
AP_Vehicle/AP_Vehicle.cpp
```

示例（节选）：

```cpp
const AP_Scheduler::Task AP_Vehicle::scheduler_tasks[] = {
    SCHED_TASK_CLASS(AP_Notify, &vehicle.notify, update, 50, 300, 78),
    SCHED_TASK(one_Hz_update, 1, 100, 252),
    SCHED_TASK_CLASS(AP_Stats, &vehicle.stats, update, 1, 100, 252),
};
```

特点：

* 明确频率（Hz）
* 明确执行预算（time budget）
* **这是飞控“正常运行状态”的调度方式**

---

### 2️⃣ `_vehicle_tasks`（Copter 专属任务）

定义位置：

```text
ArduCopter/Copter.cpp
```

通过函数注册：

```cpp
void Copter::get_scheduler_tasks(...)
```

示例（节选）：

```cpp
const AP_Scheduler::Task Copter::scheduler_tasks[] = {
    FAST_TASK(run_rate_controller_main),
    SCHED_TASK(one_hz_loop, 1, 100, 81),
    SCHED_TASK_CLASS(GCS, &_gcs, update_send, 400, 550, 105),
};
```

说明：

* `FAST_TASK`：每个 loop 都会跑（控制 / IMU）
* `SCHED_TASK`：按 Hz 调度（1Hz / 10Hz / 50Hz / 400Hz）
* **这才是飞控实时性的核心来源**

---

## 四、heartbeat


在源码中可以发现：

```cpp
GCS_SEND_MESSAGE(MSG_HEARTBEAT);
```

并不是出现在 scheduler task 中，而是在 `AP_Vehicle/AP_Vehicle.cpp` 的 `void AP_Vehicle::scheduler_delay_callback()`中出现的。

---

### ⚠️ 关键发现：scheduler_delay_callback

在 `AP_Vehicle` 初始化过程中，注册了一个 delay callback：

```cpp
hal.scheduler->register_delay_callback(
    scheduler_delay_callback, 5
);
```

回调函数：

```cpp
void AP_Vehicle::scheduler_delay_callback()
{
    if (tnow - last_1hz > 1000) {
        GCS_SEND_MESSAGE(MSG_HEARTBEAT);
        GCS_SEND_MESSAGE(MSG_SYS_STATUS);
    }
}
```

---

### 🧠 正确认知

> **scheduler_delay_callback 不是主调度机制，而是兜底机制**

它的特点：

* 只在 `Scheduler::delay()` 期间触发
* 不走 `scheduler.run()`
* 不受 task budget 控制
* 只保证“最低限度的心跳存在”

---

### ✅ 正确分层理解

```text
【正常飞控调度（主路径）】
AP_Vehicle::loop
 └─ scheduler.run
     ├─ FAST_TASK（控制 / IMU）
     ├─ 50Hz（GCS / 导航）
     ├─ 10Hz（电池 / 检查）
     └─ 1Hz（one_hz_loop / housekeeping）

【兜底机制（异常路径）】
Scheduler::delay
 └─ scheduler_delay_callback
     └─ heartbeat / sys_status
```

👉 **delay callback 是“防失联保险丝”，不是飞控主逻辑**

---

## 五、Scheduler::delay 的工作方式简析

源码核心逻辑：

```cpp
void Scheduler::delay(uint16_t ms)
{
    do {
        microsleep(...);
        if (in_main_thread()) {
            call_delay_cb();
        }
    } while (now < end);
}
```

关键点：

* 并非忙等
* 每次 sleep 后调用 delay callback
* 确保在阻塞期间：

  * GCS 不断联
  * 地面站仍能收到心跳

---