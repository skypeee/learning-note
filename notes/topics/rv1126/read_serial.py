#!/usr/bin/env python3
import serial
import sys
import time
import struct
import fcntl

PORT = "/dev/tty.usbmodem5B7E0021471"
BAUD = 1500000

# macOS specific: IOSSIOSPEED ioctl for non-standard baud rates
IOSSIOSPEED = 0x80045402

ser = serial.Serial()
ser.port = PORT
ser.baudrate = BAUD
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 0.1
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False

ser.open()

# Force macOS to use exact baud rate via ioctl
try:
    buf = struct.pack('I', BAUD)
    fcntl.ioctl(ser.fd, IOSSIOSPEED, buf)
    print(f"Forced baud rate to {BAUD} via ioctl")
except Exception as e:
    print(f"ioctl warning: {e}")

# Toggle DTR to wake up some devices
ser.dtr = False
ser.rts = False
time.sleep(0.1)
ser.dtr = True
ser.rts = True

print(f"Opened {PORT} at {BAUD} baud.")
print("Press Ctrl+C to exit.\n")

try:
    while True:
        data = ser.read(4096)
        if data:
            sys.stdout.buffer.write(data)
            sys.stdout.flush()
except KeyboardInterrupt:
    print("\nExiting.")
finally:
    ser.close()
