# MavProxy

## 示例

1. 切换到 GUIDED 模式，启动油门，然后起飞，起飞必须在启动后 15 秒内开始，否则电机将解除启动。：

```bash
mode guided
arm throttle
takeoff 40
```


2. 切换到 CIRCLE 模式并将半径设置为 2000 厘米。

```bash
rc 3 1500
mode circle
param set circle_radius 2000
```

rc 4 1000 → 最大左偏航
rc 4 2000 → 最大右偏航
rc 4 1500 → 偏航中点（不旋转）

| 通道 | 名称     | 功能                   |
| ------ | ---------- | ------------------------ |
| RC1  | Roll     | 左右倾斜               |
| RC2  | Pitch    | 前后倾斜               |
| RC3  | Throttle | 油门高度               |
| RC4     | Yaw         | 旋转方向 |


3. 降落：

```bash
mode rtl
```

4. 可以在 MAVProxy 里直接查：

```bash
help rc
```

它会显示你当前 MAVProxy 版本支持的 rc 命令格式。


5. message 模式

module load message

| Example MAVProxy/SITL Command MAVProxy/SITL 命令示例 | Description  描述                                                                                  |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `message REQUEST_DATA_STREAM 1 0 1 5 1`                                                     | Request sysid:1, compid:0 send sensor data at 5hz 请求 sysid:1, compid:0 以 5Hz 频率发送传感器数据 |
| `message REQUEST_DATA_STREAM 1 0 1 0 0`                                                     | Request sysid:1, compid:0 stop sending sensor data 请求 sysid:1, compid:0 停止发送传感器数据       |
| `message REQUEST_DATA_STREAM 1 0 6 5 1`                                                     | Request sysid:1, compid:0 send position data at 5hz 请求 sysid:1, compid:0 以 5Hz 频率发送位置数据 |
| `message REQUEST_DATA_STREAM 1 0 6 0 0`                                                     | Request sysid:1, compid:0 stop sending position data 请求 sysid:1, compid:0 停止发送位置数据       |