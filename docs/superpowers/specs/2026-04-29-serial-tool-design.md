# 串口调试工具设计文档

> 日期：2026-04-29
> 目标：合并 read_serial.py 和 shell.py 为一个交互式串口调试工具

## 背景

当前有两个独立脚本：
- `read_serial.py`：只读监控，端口和波特率硬编码
- `shell.py`：交互 Shell，端口和波特率硬编码

痛点：端口经常变（换板子/换线）、不同板子波特率不同、两个脚本来回切、日志无法保存

## 设计

### 方案：交互式菜单 + 命令行参数覆盖

默认交互式，零配置启动；支持 `--port`/`--baud`/`--mode`/`--log` 参数覆盖。

### 启动流程

```
$ python3 serial_tool.py

[串口扫描]
1. /dev/tty.usbmodem5B7E0021471  (WCH)
2. /dev/tty.usbmodem5B7E0034     (CP2102)

选择串口 [1-2]: 1

[波特率探测]
测试 1500000... ✓ 收到有效数据
波特率: 1500000

[模式选择]
1. 只读监控 (monitor)
2. 交互 Shell (shell)

选择模式 [1-2]: 2

日志保存至: logs/2026-04-29_143022_usbmodem5B7E0021471.log
Connected. Press Ctrl+] to exit.

#
```

### 功能规格

#### 1. 串口扫描

- 使用 `serial.tools.list_ports.comports()`
- 显示：序号 + 设备路径 + 芯片描述（manufacturer/VID 识别）
- 无串口时打印提示并退出
- 仅有一个串口时自动选中，跳过选择

#### 2. 波特率自动探测

- 探测顺序：1500000 → 921600 → 115200
- 每个波特率读取 2 秒，检测是否收到可打印 ASCII 字符（比例 > 60% 视为有效）
- macOS 通过 `IOSSIOSPEED` ioctl 强制设置非标准波特率
- 全部失败则回退 1500000 并警告
- 命令行指定 `--baud` 时跳过探测

#### 3. 模式选择

- `[1] 只读监控`：单向读取 + 带时间戳打印，Ctrl+C 退出
- `[2] 交互 Shell`：双向通信，终端 raw 模式，Ctrl+] 退出（保留 Ctrl+C 给板端 shell）
- 命令行指定 `--mode monitor/shell` 时跳过选择

#### 4. 日志保存

- 自动创建 `logs/` 目录（相对于脚本所在目录）
- 文件名：`YYYY-MM-DD_HHMMSS_<port简称>.log`
- 每行数据前加时间戳 `[HH:MM:SS.mmm]`
- 退出时打印日志文件路径
- `--no-log` 可禁用日志

### 命令行参数

```
python3 serial_tool.py [--port PORT] [--baud BAUD] [--mode monitor|shell] [--no-log]
```

不传参数时全部走交互式菜单。

### 退出处理

- 只读模式：Ctrl+C → 恢复终端 → 关闭串口 → 打印日志路径
- 交互模式：Ctrl+] → 恢复终端 → 关闭串口 → 打印日志路径
- 任何模式：始终在 finally 中恢复终端设置和关闭串口

### 依赖

- Python 3.8+
- pyserial（`pip3 install pyserial`）
- 无其他第三方依赖
