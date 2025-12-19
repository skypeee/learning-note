# Day 1｜ArduPilot SITL 搭建 及程序入口分析

> 目标：
> **验证 ArduPilot 飞控在最小条件下“是活着的”**，并搞清楚它真正的程序入口、主循环与 heartbeat 的来源。

---

## 一、实验目标

我们今天只回答一个问题：

> **飞控“活着”的最小条件是什么？**

飞控不关心：

* 电机
* 传感器精度
* 飞不飞

只关心三件事：

1. 程序是否在持续运行（主循环）
2. 是否对外周期性发状态（heartbeat）
3. 是否存在通信通道（UDP / 串口）

---

## 二、ArduPilot 拉取与 SITL 编译运行

### 1. 安装 Git

```bash
sudo apt-get install git
```

---

### 2. 拉取 ArduPilot 主仓库与子模块

```bash
git clone https://github.com/ArduPilot/ardupilot.git
cd ardupilot
git submodule update --init --recursive
```

---

### 3. 配置环境变量（autotest 工具）

```bash
export PATH=$PATH:<ardupilot-code-path>/Tools/autotest/
```

加入 `~/.bashrc` 后：

```bash
source ~/.bashrc
```

---

### 4. 安装依赖与工具链

```bash
Tools/environment_install/install-prereqs-ubuntu.sh -y
```

完成后加载环境：

```bash
. ~/.profile
```

---

### 5. 编译固件

#### 编译 SITL 版本（仿真）

```bash
./waf configure --board sitl
./waf copter
```

#### 编译 Pixhawk6C（实体板）

```bash
./waf configure --board Pixhawk6C
./waf copter
```

---

### 6. 运行仿真飞控

```bash
sim_vehicle.py -v ArduCopter
```

常用参数：

* `--console`：自动启动 MAVProxy 控制台
* `--map`：启动 2D 地图
* `-L KSFO`：设置起飞位置

此时表现为：

* 程序不退出
* 初始化日志持续输出

这已经说明：**飞控主循环在运行**。

---

## 三、为什么“看不到 heartbeat”？

### 1. 日志 ≠ Heartbeat

终端中反复出现的：

```
Flight battery 100 percent
```

这是 **STATUSTEXT**，不是 heartbeat。

* STATUSTEXT：文本日志，MAVProxy 默认打印
* HEARTBEAT：二进制 MAVLink 消息，默认不刷屏

---

### 2. MAVProxy 中验证 heartbeat

在 MAVProxy 控制台输入：

```text
watch HEARTBEAT
```

即可看到：

```
< HEARTBEAT {type : 2, autopilot : 3, base_mode : 81, ...}
```

这说明：

> **飞控正在以 1Hz 周期发送 heartbeat**。

---

### 3. 使用 Python 验证 heartbeat

```python
msg = master.recv_match(type='HEARTBEAT', blocking=True)
print(msg)
```

结论一致：heartbeat 确实存在。

---

## 四、ArduPilot 真正的程序入口在哪里？

### 1. Copter.cpp 中的“入口宏”

```cpp
Copter copter;
AP_Vehicle& vehicle = copter;

AP_HAL_MAIN_CALLBACKS(&copter);
```

这并不是普通的 `main()`，而是一个宏。

---

### 2. AP_HAL_MAIN_CALLBACKS 宏展开（AP_HAL.h）

```cpp
#define AP_HAL_MAIN_CALLBACKS(CALLBACKS) extern "C" { \
    int AP_MAIN(int argc, char* const argv[]); \
    int AP_MAIN(int argc, char* const argv[]) { \
        hal.run(argc, argv, CALLBACKS); \
        return 0; \
    } \
}
```

> **真正的 main() 是由 HAL 生成的**。

---

### 3. HAL_Linux::run 中的核心逻辑

```cpp
callbacks->setup();

while (!_should_exit) {
    callbacks->loop();
}
```

这里明确表明：

* setup() 只执行一次
* loop() 由 HAL 驱动，持续运行

---

### 4. setup / loop 来自哪里？

* `Copter` 继承自 `AP_Vehicle`
* `AP_Vehicle` 定义虚函数 `setup()` / `loop()`
* Copter 重写并实现它们

> **飞控的“生命函数”是 Copter::setup() 和 Copter::loop()**

---

## 五、核心结论

### 飞控“活着”的最小条件

只需要三件事：

1. **HAL 创建 main 并调度 loop**
2. **loop 持续运行，不退出**
3. **MAVLink 周期性发送 heartbeat**

不依赖：

* 电机
* GPS
* IMU
* 遥控器
