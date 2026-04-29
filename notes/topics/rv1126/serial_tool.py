#!/usr/bin/env python3
"""串口调试工具 — 自动扫描、探测波特率、只读/交互、日志保存"""

import serial
import serial.tools.list_ports
import struct
import fcntl
import sys
import os
import termios
import tty
import threading
import time
import argparse
from datetime import datetime

IOSSIOSPEED = 0x80045402
PROBE_BAUDS = [1500000, 921600, 115200]
PROBE_TIMEOUT = 2  # seconds per baud rate


def scan_ports():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("未检测到串口设备。")
        sys.exit(1)
    return ports


def choose_port(ports, preset=None):
    if preset:
        matching = [p for p in ports if preset in p.device]
        if matching:
            return matching[0].device
        print(f"未找到匹配 {preset} 的串口。")

    if len(ports) == 1:
        p = ports[0]
        desc = p.manufacturer or p.description or ""
        print(f"自动选中: {p.device}  ({desc})")
        return p.device

    print("\n[串口扫描]")
    for i, p in enumerate(ports, 1):
        desc = p.manufacturer or p.description or ""
        print(f"  {i}. {p.device}  ({desc})")

    while True:
        try:
            choice = input(f"选择串口 [1-{len(ports)}]: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(ports):
                return ports[idx].device
        except (ValueError, EOFError):
            pass
        print("无效选择，请重试。")


def open_serial(device, baud):
    ser = serial.Serial()
    ser.port = device
    ser.baudrate = baud
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 0.1
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False
    ser.open()

    if sys.platform == "darwin":
        try:
            buf = struct.pack('I', baud)
            fcntl.ioctl(ser.fd, IOSSIOSPEED, buf)
        except Exception:
            pass

    ser.dtr = False
    ser.rts = False
    time.sleep(0.1)
    ser.dtr = True
    ser.rts = True
    return ser


def probe_baud(device, preset=None):
    if preset:
        print(f"使用指定波特率: {preset}")
        return preset

    print("\n[波特率探测]")
    for baud in PROBE_BAUDS:
        print(f"  测试 {baud}...", end=" ", flush=True)
        try:
            ser = open_serial(device, baud)
            # Send enter to wake up the shell (board may be idle)
            time.sleep(0.3)
            ser.write(b"\n")
            ser.flush()
            buf = bytearray()
            deadline = time.time() + PROBE_TIMEOUT
            while time.time() < deadline:
                chunk = ser.read(4096)
                if chunk:
                    buf.extend(chunk)
            ser.close()

            if buf:
                printable = sum(1 for b in buf if 32 <= b <= 126 or b in (10, 13, 9))
                ratio = printable / len(buf) if buf else 0
                if ratio > 0.6:
                    print(f"✓ 有效数据 ({len(buf)} bytes, 可打印率 {ratio:.0%})")
                    return baud
                else:
                    print(f"✗ 乱码 (可打印率 {ratio:.0%})")
            else:
                print("✗ 无数据")
        except Exception as e:
            print(f"✗ 错误: {e}")

    print(f"  ⚠ 探测失败，使用默认 {PROBE_BAUDS[0]}")
    return PROBE_BAUDS[0]


def choose_mode(preset=None):
    if preset in ("monitor", "shell", "transfer"):
        return preset

    print("\n[模式选择]")
    print("  1. 只读监控 (monitor)")
    print("  2. 交互 Shell (shell)")
    print("  3. 文件传输 (transfer)")

    while True:
        try:
            choice = input("选择模式 [1-3]: ").strip()
            if choice in ("1", "m", "monitor"):
                return "monitor"
            if choice in ("2", "s", "shell"):
                return "shell"
            if choice in ("3", "t", "transfer"):
                return "transfer"
        except EOFError:
            pass
        print("无效选择，请重试。")


def setup_logging(device, enabled=True):
    if not enabled:
        return None

    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    port_name = os.path.basename(device).replace(".", "_")
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_path = os.path.join(log_dir, f"{ts}_{port_name}.log")

    return open(log_path, "wb")


def timestamp_bytes():
    now = datetime.now()
    return f"[{now.strftime('%H:%M:%S')}.{now.microsecond // 1000:03d}] ".encode()


def run_monitor(ser, log_file):
    print(f"只读模式 — Ctrl+C 退出\n")
    try:
        while True:
            data = ser.read(4096)
            if data:
                ts = timestamp_bytes()
                sys.stdout.buffer.write(ts + data)
                sys.stdout.flush()
                if log_file:
                    log_file.write(ts + data)
                    log_file.flush()
    except KeyboardInterrupt:
        pass


def run_shell(ser, log_file):
    print(f"交互模式 — Ctrl+] 退出\n")

    def reader():
        while True:
            try:
                data = ser.read(4096)
                if data:
                    sys.stdout.buffer.write(data)
                    sys.stdout.flush()
                    if log_file:
                        log_file.write(data)
                        log_file.flush()
            except Exception:
                break

    old_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    threading.Thread(target=reader, daemon=True).start()

    try:
        while True:
            ch = sys.stdin.read(1)
            if ch == '\x1d':  # Ctrl+]
                break
            ser.write(ch.encode('latin-1'))
            ser.flush()
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def main():
    parser = argparse.ArgumentParser(description="串口调试工具")
    parser.add_argument("--port", help="串口设备路径（模糊匹配）")
    parser.add_argument("--baud", type=int, help="波特率（跳过自动探测）")
    parser.add_argument("--mode", choices=["monitor", "shell", "transfer"], help="模式：monitor/shell/transfer")
    parser.add_argument("--no-log", action="store_true", help="禁用日志保存")
    args = parser.parse_args()

    ports = scan_ports()
    device = choose_port(ports, args.port)
    baud = probe_baud(device, args.baud)
    mode = choose_mode(args.mode)

    print(f"\n连接 {device} @ {baud} ...", end=" ", flush=True)
    ser = open_serial(device, baud)
    print("已连接")

    log_file = setup_logging(device, not args.no_log)
    if log_file:
        log_path = log_file.name
        print(f"日志保存至: {log_path}")
    else:
        log_path = None

    try:
        if mode == "monitor":
            run_monitor(ser, log_file)
        elif mode == "shell":
            run_shell(ser, log_file)
        elif mode == "transfer":
            ser.close()
            ser = None
            if log_file:
                log_file.close()
                log_file = None
            import subprocess
            script_dir = os.path.dirname(os.path.abspath(__file__))
            transfer_script = os.path.join(script_dir, "serial_transfer.py")
            port_arg = ["--port", os.path.basename(device)] if device else []
            subprocess.run([sys.executable, transfer_script] + port_arg + ["--baud", str(baud)])
    finally:
        if ser:
            ser.close()
        if log_file:
            log_file.close()
        print("\n已断开。")
        if log_path:
            print(f"日志文件: {log_path}")


if __name__ == "__main__":
    main()
