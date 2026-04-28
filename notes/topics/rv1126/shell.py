#!/usr/bin/env python3
import serial
import sys
import threading
import struct
import fcntl
import termios
import tty

PORT = "/dev/tty.usbmodem5B7E0021471"
BAUD = 1500000
IOSSIOSPEED = 0x80045402

ser = serial.Serial()
ser.port = PORT
ser.baudrate = BAUD
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 0.1
ser.open()

try:
    buf = struct.pack('I', BAUD)
    fcntl.ioctl(ser.fd, IOSSIOSPEED, buf)
except Exception:
    pass

ser.dtr = True
ser.rts = True

print(f"Connected to {PORT} at {BAUD} baud.")
print("Press Enter to wake up, then try typing commands.")
print("Press Ctrl+C or Ctrl+] to exit.\n")

def reader():
    while True:
        try:
            data = ser.read(4096)
            if data:
                sys.stdout.buffer.write(data)
                sys.stdout.flush()
        except Exception:
            break

old_settings = termios.tcgetattr(sys.stdin)
tty.setraw(sys.stdin.fileno())

threading.Thread(target=reader, daemon=True).start()

try:
    while True:
        ch = sys.stdin.read(1)
        if ch == '\x03':
            break
        if ch == '\x1d':
            break
        ser.write(ch.encode('latin-1'))
        ser.flush()
except KeyboardInterrupt:
    pass
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    ser.close()
    print("\nDisconnected.")
