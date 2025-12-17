# ArduPilot 自定义 MAVLink 消息并通过 SITL 与实机交互完整实践

本文记录一次 **在 ArduPilot 中自定义 MAVLink 消息，并完成 SITL 与真实飞控（Pixhawk 6C）双端验证** 的完整流程。内容以“**能复现、可验证**”为目标，适合作为后续开发和排错的技术笔记。

---

## 一、整体流程概览

整个实现流程可拆分为 6 个阶段：

1. **定义 MAVLink 消息（XML）**
2. **飞控端添加消息处理逻辑**
3. **编译 ArduPilot（SITL）**
4. **SITL + Python 端验证**
5. **编译并烧录真实飞控固件**
6. **真实飞控 + Python 通信验证**

---

## 二、定义 MAVLink 消息

编辑 ArduPilot 自带的 MAVLink 协议文件：

```bash
vim modules/mavlink/message_definitions/v1.0/ardupilotmega.xml
```

新增一条自定义消息（**注意：ID 需避免与已有消息冲突**）：

```xml
<message id="42001" name="MY_TEST_MSG">
    <description>My custom test mavlink message</description>
    <field type="uint32_t" name="time_boot_ms">Time since boot</field>
    <field type="float" name="value">Test value</field>
</message>
```

说明：

* `id=42001`：自定义消息 ID（建议选择较大的空闲 ID）
* `MY_TEST_MSG`：消息名，后续会自动生成宏和结构体
* 字段顺序 **必须与生成代码一致**，否则解析错误

---

## 三、飞控端添加消息处理逻辑

### 1. 修改消息处理入口

ArduPilot 中 **所有通用 MAVLink 消息** 都在以下函数中分发处理：

```cpp
void GCS_MAVLINK::handle_message(const mavlink_message_t &msg)
```

文件位置：

```text
libraries/GCS_MAVLink/GCS_Common.cpp
```

该函数的职责是：

> 处理不依赖具体机型（Copter / Plane / Rover）的 MAVLink 消息

### 2. 在 switch 中添加自定义 case

`MAVLINK_MSG_ID_MY_TEST_MSG` 会在编译阶段由 MAVLink 自动生成。

```cpp
case MAVLINK_MSG_ID_MY_TEST_MSG: {
    mavlink_my_test_msg_t pkt;

    GCS_SEND_TEXT(MAV_SEVERITY_INFO,
        "--------------------handle_message msgid=%u------------------------------",
        msg.msgid);

    // 解码收到的消息
    mavlink_msg_my_test_msg_decode(&msg, &pkt);

    GCS_SEND_TEXT(MAV_SEVERITY_INFO,
        "recv MY_TEST_MSG %.2f",
        pkt.value);

    // 回发一条 MY_TEST_MSG，用于验证双向通信
    mavlink_msg_my_test_msg_send(
        chan,
        AP_HAL::millis(),
        123.0f
    );
    break;
}
```

说明：

* `decode`：解析来自地面站 / Python 的消息
* `send`：用于验证飞控 → 地面端通信是否正常
* `chan`：当前 MAVLink 通道

---

## 四、编译 ArduPilot（SITL）

```bash
./waf configure --board sitl
./waf copter
```

编译完成后即可启动 SITL。

---

## 五、SITL 验证

### 1. 启动仿真环境

```bash
sim_vehicle.py -v Copter --console --map
```

### 2. Python 端发送 / 接收自定义消息

```python
from pymavlink import mavutil

master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
master.wait_heartbeat()

# 发送自定义消息
master.mav.my_test_msg_send(
    100,
    6.66
)

# 接收飞控回传
while True:
    msg = master.recv_match(type='MY_TEST_MSG', blocking=True)
    print("msg is : ", msg)
```

---

## 六、重新生成 pymavlink（关键步骤）

**只要修改了 MAVLink XML，就必须重新生成 pymavlink，否则 Python 端无法识别新消息。**

### 1. 获取 pymavlink 源码

```bash
cd ~/workspace
git clone https://github.com/ArduPilot/pymavlink.git
cd pymavlink
```

### 2. 指定 MAVLink 协议配置

```bash
export MAVLINK_DIALECT=ardupilotmega
export MAVLINK10=0
```

### 3. 让 pymavlink 使用你修改过的 XML

最简单方式：创建软链接

```bash
ln -s ~/workspace/ardupilot/modules/mavlink/message_definitions .
```

目录结构应为：

```text
pymavlink/
└── message_definitions/
    └── v1.0/
        └── ardupilotmega.xml  # 含 MY_TEST_MSG
```

### 4. 重新生成并安装

```bash
python3 -m pip install . --user
```

### 5. SITL 端验证结果

```text
msg is :  MY_TEST_MSG {time_boot_ms : 57029, value : 123.0}
```

说明：

* Python → SITL → Python **双向通信成功**

---

## 七、编译并烧录真实飞控（Pixhawk 6C）

### 1. 编译固件

```bash
./waf configure --board Pixhawk6C
./waf copter
```

生成的固件路径：

```text
build/Pixhawk6C/bin/arducopter.apj
```

### 2. 烧录到飞控

使用 Mission Planner / QGC 烧录该 `arducopter.apj` 文件。

---

## 八、真实飞控通信验证

### Python 测试脚本

```python
from pymavlink import mavutil

print("Connecting to Pixhawk6C...")
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=921600)

print("Waiting for heartbeat...")
master.wait_heartbeat()
print(f"✅ Connected! System: {master.target_system}, Component: {master.target_component}")

# 发送自定义消息
try:
    master.mav.my_test_msg_send(
        100,
        6.66
    )
    print("📤 Sent MY_TEST_MSG")
except AttributeError:
    print("❌ pymavlink 未包含自定义消息，请重新生成")
    exit(1)

print("Listening for MY_TEST_MSG replies (5-second timeout)...")
msg = master.recv_match(type='MY_TEST_MSG', blocking=True, timeout=5)

if msg:
    print("📩 Received reply:", msg)
else:
    print("⏳ No reply received")
```

### 成功输出示例

```text
Connecting to Pixhawk6C...
Waiting for heartbeat...
✅ Connected! System: 1, Component: 0
📤 Sent MY_TEST_MSG
Listening for MY_TEST_MSG replies (5-second timeout)...
📩 Received reply: MY_TEST_MSG {time_boot_ms : 11635, value : 123.0}
```

说明：

* Python ↔ 飞控 **双向通信完全打通**
* 自定义 MAVLink 消息在实机上工作正常

---

## 九、关键注意事项总结

* **修改 XML 后必须：**

  * 重新编译 ArduPilot
  * 重新生成 pymavlink
* 消息 ID 不可冲突
* 字段顺序和类型必须完全一致
* 串口波特率需与飞控一致（Pixhawk 6C 常用 921600）
* `handle_message` 只处理通用消息，机型相关消息应放在对应模块

---

## 十、下一步可扩展方向

* 将消息处理拆分为独立模块（避免 GCS_Common.cpp 过大）
* 加入 ACK / 状态机协议
* 与 Mission Planner / QGC 插件联动
* 用于 **自定义传感器 / AI / Companion Computer 通信**

---

> 本文档完整记录了一条 MAVLink 自定义消息从 **XML → SITL → 实机** 的全链路实践，可作为后续 MAVLink 深度开发的基础模板。
