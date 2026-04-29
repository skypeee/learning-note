#!/usr/bin/env python3
"""串口文件传输 — 通过串口 shell 推送/拉取文件和目录"""

import serial
import serial.tools.list_ports
import struct
import fcntl
import sys
import os
import subprocess
import tempfile
import base64
import time
import argparse

IOSSIOSPEED = 0x80045402
CHUNK_SIZE = 3072  # base64 lines per chunk (~3KB raw each)
COMMAND_DELAY = 0.05  # delay between chunks to avoid buffer overflow


def open_serial(device, baud):
    ser = serial.Serial()
    ser.port = device
    ser.baudrate = baud
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 0.5
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


def drain(ser, timeout=1.0):
    """Read and discard all pending data."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = ser.read(4096)
        if not data:
            break


def send_cmd(ser, cmd, wait=0.3):
    """Send a shell command and wait for response."""
    ser.write((cmd + "\n").encode())
    ser.flush()
    time.sleep(wait)
    return ser.read(4096)


def wait_for_prompt(ser, timeout=5.0):
    """Wait until we see a shell prompt (# or $)."""
    deadline = time.time() + timeout
    buf = b""
    while time.time() < deadline:
        data = ser.read(4096)
        if data:
            buf += data
            if buf.rstrip().endswith(b"#") or buf.rstrip().endswith(b"$"):
                return True
    return False


def ensure_shell(ser):
    """Make sure we have an active shell on the board."""
    drain(ser)
    # Send enter to wake up the shell (board may be waiting for input)
    time.sleep(0.5)
    ser.write(b"\n")
    ser.flush()
    time.sleep(0.5)
    drain(ser, 0.5)
    ser.write(b"\n")
    ser.flush()
    time.sleep(0.5)
    drain(ser, 0.5)
    send_cmd(ser, "echo READY_SERIAL", 0.5)
    resp = b""
    deadline = time.time() + 3.0
    while time.time() < deadline:
        data = ser.read(4096)
        if data:
            resp += data
            if b"READY_SERIAL" in resp:
                return True
    return False


def push_file(ser, local_path, remote_path):
    """Push a single file to the board via base64 encoding."""
    file_size = os.path.getsize(local_path)
    print(f"  推送: {local_path} → {remote_path} ({file_size} bytes)")

    # Create remote directory
    remote_dir = os.path.dirname(remote_path)
    if remote_dir:
        send_cmd(ser, f"mkdir -p {remote_dir}", 0.3)

    # Start base64 decode on board
    send_cmd(ser, f"base64 -d > {remote_path} << 'ENDOFBASE64'", 0.3)

    # Send file in base64 chunks
    sent = 0
    with open(local_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            encoded = base64.b64encode(chunk)
            ser.write(encoded + b"\n")
            ser.flush()
            sent += len(chunk)
            pct = sent * 100 // file_size if file_size else 100
            print(f"\r  进度: {sent}/{file_size} ({pct}%)", end="", flush=True)
            time.sleep(COMMAND_DELAY)

    # End base64 input
    ser.write(b"ENDOFBASE64\n")
    ser.flush()
    time.sleep(0.5)
    drain(ser, 1.0)

    # Verify file size
    resp = send_cmd(ser, f"stat -c %s {remote_path} 2>/dev/null || echo FAIL", 0.5)
    remote_size = resp.decode(errors="replace").strip().split("\n")[-1].strip()
    if remote_size.isdigit() and int(remote_size) == file_size:
        print(f"\r  ✓ 完成 ({file_size} bytes)          ")
    else:
        print(f"\r  ⚠ 本地 {file_size} bytes, 远端 {remote_size} bytes")


def push_dir(ser, local_dir, remote_dir):
    """Push a directory by creating tar.gz, sending, and extracting on board."""
    # Create temp tar.gz
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp_path = tmp.name

    print(f"  打包: {local_dir} → tar.gz")
    subprocess.run(["tar", "czf", tmp_path, "-C", os.path.dirname(local_dir), os.path.basename(local_dir)],
                   check=True, capture_output=True)
    archive_size = os.path.getsize(tmp_path)

    # Create remote dir
    send_cmd(ser, f"mkdir -p {remote_dir}", 0.3)

    # Push archive
    remote_archive = f"/tmp/_serial_push_{int(time.time())}.tar.gz"
    push_file(ser, tmp_path, remote_archive)

    # Extract on board
    print(f"  解压: {remote_archive} → {remote_dir}")
    send_cmd(ser, f"tar xzf {remote_archive} -C {remote_dir}", 1.0)
    send_cmd(ser, f"rm -f {remote_archive}", 0.3)
    drain(ser, 0.5)

    os.unlink(tmp_path)
    print(f"  ✓ 目录推送完成")


def pull_file(ser, remote_path, local_path):
    """Pull a single file from the board via base64 encoding."""
    # Check if remote file exists and get size
    resp = send_cmd(ser, f"stat -c %s {remote_path} 2>/dev/null || echo FAIL", 0.5)
    size_str = resp.decode(errors="replace").strip().split("\n")[-1].strip()
    if size_str == "FAIL" or not size_str.isdigit():
        print(f"  ✗ 远端文件不存在: {remote_path}")
        return
    remote_size = int(size_str)
    print(f"  拉取: {remote_path} → {local_path} ({remote_size} bytes)")

    # Create local directory
    local_dir = os.path.dirname(local_path)
    if local_dir:
        os.makedirs(local_dir, exist_ok=True)

    # Send base64 encode command
    send_cmd(ser, f"base64 {remote_path}", 0.3)
    time.sleep(0.2)

    # Read base64 data
    buf = b""
    deadline = time.time() + max(10, remote_size / 5000)  # rough timeout
    while time.time() < deadline:
        data = ser.read(4096)
        if data:
            buf += data
            # Check if we got a prompt back (transfer complete)
            if buf.rstrip().endswith(b"#") or buf.rstrip().endswith(b"$"):
                break

    # Parse: skip command echo, extract base64 lines until prompt
    lines = buf.decode(errors="replace").split("\n")
    b64_lines = []
    started = False
    for line in lines:
        stripped = line.strip()
        if not started:
            if "base64" in stripped:
                started = True
            continue
        if stripped.endswith("#") or stripped.endswith("$") or stripped == "":
            if b64_lines:
                continue
        b64_lines.append(stripped)

    try:
        file_data = base64.b64decode("".join(b64_lines))
        with open(local_path, "wb") as f:
            f.write(file_data)
        actual_size = len(file_data)
        print(f"  ✓ 完成 ({actual_size} bytes)")
    except Exception as e:
        print(f"  ✗ 解码失败: {e}")


def pull_dir(ser, remote_dir, local_dir):
    """Pull a directory by creating tar.gz on board, pulling, and extracting locally."""
    print(f"  打包远端: {remote_dir}")
    remote_archive = f"/tmp/_serial_pull_{int(time.time())}.tar.gz"
    send_cmd(ser, f"tar czf {remote_archive} -C {os.path.dirname(remote_dir)} {os.path.basename(remote_dir)}", 1.0)
    drain(ser, 0.5)

    # Pull archive
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp_path = tmp.name

    pull_file(ser, remote_archive, tmp_path)

    # Extract locally
    print(f"  解压: {tmp_path} → {local_dir}")
    os.makedirs(local_dir, exist_ok=True)
    subprocess.run(["tar", "xzf", tmp_path, "-C", local_dir], check=True, capture_output=True)

    # Cleanup
    send_cmd(ser, f"rm -f {remote_archive}", 0.3)
    os.unlink(tmp_path)
    print(f"  ✓ 目录拉取完成")


def choose_direction():
    print("\n[传输方向]")
    print("  1. 推送 (push)  — 本地 → 板子")
    print("  2. 拉取 (pull)  — 板子 → 本地")

    while True:
        try:
            choice = input("选择方向 [1-2]: ").strip()
            if choice in ("1", "p", "push"):
                return "push"
            if choice in ("2", "g", "pull"):
                return "pull"
        except EOFError:
            pass
        print("无效选择，请重试。")


def main():
    parser = argparse.ArgumentParser(description="串口文件传输")
    parser.add_argument("--port", help="串口设备路径（模糊匹配）")
    parser.add_argument("--baud", type=int, default=1500000, help="波特率")
    parser.add_argument("--push", help="推送本地文件/目录到板子")
    parser.add_argument("--pull", help="从板子拉取文件/目录到本地")
    parser.add_argument("--remote", help="板子上的目标路径")
    parser.add_argument("--direction", choices=["push", "pull"], help="传输方向")
    args = parser.parse_args()

    # Scan and select port
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("未检测到串口设备。")
        sys.exit(1)

    if args.port:
        matching = [p for p in ports if args.port in p.device]
        if matching:
            device = matching[0].device
        else:
            print(f"未找到匹配 {args.port} 的串口。")
            sys.exit(1)
    elif len(ports) == 1:
        device = ports[0].device
        desc = ports[0].manufacturer or ports[0].description or ""
        print(f"自动选中: {device}  ({desc})")
    else:
        print("[串口扫描]")
        for i, p in enumerate(ports, 1):
            desc = p.manufacturer or p.description or ""
            print(f"  {i}. {p.device}  ({desc})")
        while True:
            try:
                choice = input(f"选择串口 [1-{len(ports)}]: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(ports):
                    device = ports[idx].device
                    break
            except (ValueError, EOFError):
                pass

    baud = args.baud
    print(f"\n连接 {device} @ {baud} ...", end=" ", flush=True)
    ser = open_serial(device, baud)
    print("已连接")

    # Ensure shell is active
    print("等待 shell ...", end=" ", flush=True)
    if not ensure_shell(ser):
        print("✗ 无法获取 shell，请确认板子已启动且串口可交互")
        ser.close()
        sys.exit(1)
    print("就绪")

    try:
        direction = args.direction
        if not direction:
            if args.push:
                direction = "push"
            elif args.pull:
                direction = "pull"
            else:
                direction = choose_direction()

        if direction == "push":
            local_path = args.push or input("本地文件/目录路径: ").strip()
            remote_path = args.remote or input("板子目标路径: ").strip()
            if not os.path.exists(local_path):
                print(f"✗ 本地路径不存在: {local_path}")
                return
            if os.path.isdir(local_path):
                push_dir(ser, local_path, remote_path)
            else:
                push_file(ser, local_path, remote_path)

        elif direction == "pull":
            remote_path = args.pull or input("板子文件/目录路径: ").strip()
            local_path = args.remote or input("本地保存路径: ").strip()
            # Check if remote is file or dir
            resp = send_cmd(ser, f"test -d {remote_path} && echo DIR || echo FILE", 0.5)
            resp_str = resp.decode(errors="replace")
            if "DIR" in resp_str:
                pull_dir(ser, remote_path, local_path)
            else:
                pull_file(ser, remote_path, local_path)

    finally:
        ser.close()
        print("\n已断开。")


if __name__ == "__main__":
    main()
