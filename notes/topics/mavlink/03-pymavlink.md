# 🛰️ ArduPilot SITL + pymavlink 通信测试


> **目标**：在 ArduPilot 的 SITL（Software-In-The-Loop）仿真环境中，  
> ✅ 通过 MAVLink 读取飞控数据（姿态、电池等）  
> ✅ 发送自定义 MAVLink 命令并验证飞控响应  

---

## 🧰 一、环境准备

### 1. 软件依赖
- **ArduPilot 源码**
  ```bash
  git clone https://github.com/ArduPilot/ardupilot.git
  cd ardupilot
  git submodule update --init --recursive
  ```
- **Python 库**
  ```bash
  pip install pymavlink pyserial
  ```

### 2. 启动 SITL（以 Copter 为例）
```bash
cd ardupilot
sim_vehicle.py -v ArduCopter --console --map
```
- 默认开启 TCP 端口：`127.0.0.1:5760` 或者UDP端口 `udp:127.0.0.1:14550`
- 飞控系统 ID = 1，组件 ID = 0（ArduPilot 的 autopilot 组件）
---

## 📡 二、Python 脚本：连接 + 读取 + 发送

### 完整脚本：`test_ardupilot_sitl.py`

```python
from pymavlink import mavutil
import time

# === 1. 连接 SITL ===
print("Connecting to ArduPilot SITL...")
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
master.wait_heartbeat()
print(f"Heartbeat from system {master.target_system}, component {master.target_component}")

# === 2. 请求特定消息流（提高更新频率）===
def request_message_interval(message_id: int, interval_us: int):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
        0,
        message_id,
        interval_us,
        0, 0, 0, 0, 0
    )

# 请求 ATTITUDE（~30Hz）和 BATTERY_STATUS（1Hz）
request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE, 33333)
request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_BATTERY_STATUS, 1000000)

# === 3. 发送自定义命令（测试下行链路）===
print("\nSending custom command: DO_SEND_BANNER...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_SEND_BANNER,  # 命令ID: 176
    0, 0, 0, 0, 0, 0, 0, 0
)

# === 4. 监听并解析数据 ===
print("\nListening for ATTITUDE and BATTERY_STATUS...\n")
start_time = time.time()
try:
    while time.time() - start_time < 10:  # 运行10秒
        msg = master.recv_match(type=['ATTITUDE', 'BATTERY_STATUS'], blocking=True, timeout=1)
        if not msg:
            continue

        if msg.get_type() == 'ATTITUDE':
            print(f"[ATTITUDE] Roll: {msg.roll:.2f} rad, Pitch: {msg.pitch:.2f}, Yaw: {msg.yaw:.2f}")
        
        elif msg.get_type() == 'BATTERY_STATUS':
            voltage_mv = msg.voltages[0]  # ⚠️ 注意：MAVLink 2 使用 voltages[0]
            if voltage_mv != 65535:       # 65535 = 无效值
                voltage_v = voltage_mv / 1000.0
                current_a = msg.current_battery / 100.0 if msg.current_battery != -1 else 0
                print(f"[BATTERY] Voltage: {voltage_v:.2f} V, Current: {current_a:.1f} A")
            else:
                print("[BATTERY] Invalid data")

except KeyboardInterrupt:
    pass

print("\n✅ Test completed.")
```

---

## ✅ 三、关键知识点说明

### 1. **MAVLink 版本差异（重要！）**

| 字段 | MAVLink 1 | MAVLink 2（ArduPilot 默认） |
|------|-----------|----------------------------|
| 电池电压 | `voltage_battery` (mV) | `voltages[0]` (mV) |
| 电流 | `current_battery` (cA) | `current_battery` (cA) |

> ❗ 错误示例：
> ```python
> msg.voltage_battery  # AttributeError in ArduPilot SITL!
> ```
> ✅ 正确用法：
> ```python
> msg.voltages[0]  # 总电压（毫伏）
> ```

### 2. **常用 MAVLink 消息 ID**
| 消息名 | ID | 用途 |
|--------|----|------|
| `HEARTBEAT` | 0 | 心跳包，包含飞控状态、模式 |
| `ATTITUDE` | 30 | 姿态（roll/pitch/yaw，单位：弧度） |
| `BATTERY_STATUS` | 147 | 电池电压、电流、剩余电量 |
| `GPS_RAW_INT` | 24 | GPS 原始数据 |

### 3. **自定义命令选项**
| 命令 | ID | 说明 |
|------|----|------|
| `MAV_CMD_DO_SEND_BANNER` | 176 | 测试命令，飞控会向 GCS 发送 banner |
| `MAV_CMD_USER_1` | 31001 | 用户自定义命令（需 Lua 脚本监听） |
| `MAV_CMD_USER_2~4` | 31002~31004 | 同上 |

---

## 🧪 四、测试结果验证

### 成功标志 ✅
- 输出包含：
  ```
  [ATTITUDE] Roll: 0.00 rad, Pitch: 0.00, Yaw: -0.13
  [BATTERY] Voltage: 12.60 V, Current: 28.1 A
  ```
- SITL 控制台显示 `Sent banner to GCS`（证明命令被接收）

### 组件 ID 注意
- ArduPilot 的 autopilot 组件 ID 是 **0**
- PX4 的 autopilot 组件 ID 是 **1**
- 所以 `master.target_component == 0` 表示连接的是 ArduPilot

---

> ✍️ **记录人**：Shikun  
> 📅 **日期**：2025-12-15  
> 💡 **备注**：此流程已在 Ubuntu + ArduPilot v4.5+ SITL 环境验证通过
