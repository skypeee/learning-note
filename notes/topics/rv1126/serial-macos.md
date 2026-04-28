# RV1126B 串口调试笔记（macOS）

## 问题描述

正点原子 RV1126B 开发板，在 macOS 上通过串口读取不到任何数据：

```bash
screen /dev/tty.usbmodem5B7E0021471 1500000
```

串口存在、权限正常，但完全没有输出。

## 环境信息

- **主机**: macOS
- **板子**: 正点原子 RV1126B
- **串口芯片**: WCH（沁恒微），VID=0x1A86
- **串口设备**: `/dev/tty.usbmodem5B7E0021471`
- **调试串口波特率**: 1500000（1.5 Mbps）

## 排查过程

### 1. 检查串口是否存在及权限

```bash
ls -la /dev/tty.usbmodem5B7E0021471
# crw-rw-rw- 1 root wheel ... 权限正常

stty -f /dev/tty.usbmodem5B7E0021471
# speed 9600 baud; 当前被系统默认成了 9600
```

### 2. 检查波特率

RV1126 的调试串口通常是 **1500000**，但 macOS 对非标准波特率支持很差。

- 标准波特率：9600, 115200, 230400, 460800, 921600 等
- **1500000 不在标准列表中**

用 Python 脚本依次测试多个波特率，发现：

- 115200 → 收到乱码（说明有数据，但速率不对）
- 921600 → 收到乱码
- **1500000 → 收到正常 boot log**

### 3. 根本原因

macOS 的 `screen`、`cu`、`minicom` 等工具底层走标准的 `tcsetattr` 接口设置波特率。

**当波特率超过 230400 时，macOS 会静默 fallback 到 9600 或 115200**，不会报错，但通信必然失败。

而 Python + `pyserial` 可以通过 **macOS 私有 ioctl `IOSSIOSPEED`** 强制设置精确波特率，绕过标准限制。

## 解决方案

### 安装依赖

```bash
pip3 install pyserial
```

### 串口读取脚本（只读）

见同目录 `read_serial.py`。

### 串口交互脚本（双向，可进 shell）

见同目录 `shell.py`。

### 使用方法

```bash
python3 shell.py
```

板子启动完成后按 **回车**，即可进入 shell 交互。

正点原子 buildroot 默认：
- 用户名：`root`
- 密码：空（直接回车）

## 内核日志静音

进入 shell 后，内核日志会一直刷到串口，影响使用。关闭方法：

```bash
# 临时关闭（推荐，可随时恢复）
dmesg -n 1

# 或者
echo 1 > /proc/sys/kernel/printk
```

恢复日志输出：

```bash
dmesg -n 7
```

### 开机默认静音（可选）

在 uboot 命令行修改 bootargs（重启时按 `Ctrl+C` 打断 autoboot）：

```bash
setenv bootargs "... quiet loglevel=1"
saveenv
reset
```

## 关键结论

| 问题 | 原因 | 解决 |
|------|------|------|
| screen 读不到数据 | macOS `tcsetattr` 不支持 1500000，静默 fallback | 用 Python + `IOSSIOSPEED` ioctl |
| 波特率不确定 | RV1126 不同固件版本可能不同 | 依次测试 115200 / 921600 / 1500000 |
| 内核日志刷屏 | `printk` 默认输出到 console | `dmesg -n 1` 临时关闭 |

## 参考

- `IOSSIOSPEED` 定义: `0x80045402`
- 芯片 VID: `0x1A86`（WCH 沁恒微）
- 板子型号: `ALIENTEK RV1126B board`
