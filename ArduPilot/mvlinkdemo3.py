# from pymavlink import mavutil
# import time

# COM_PORT = 'COM3'
# BAUD_RATE = 115200

# print(f"Connecting to {COM_PORT} @ {BAUD_RATE}...")
# try:
#     # 创建连接，带 timeout 防止卡死
#     master = mavutil.mavlink_connection(COM_PORT, baud=BAUD_RATE, timeout=3)
    
#     print("Waiting for heartbeat (max 10s)...")
#     start_time = time.time()
#     while time.time() - start_time < 10:
#         msg = master.recv_msg()
#         if msg is None:
#             continue
        
#         if msg.get_type() == 'HEARTBEAT':
#             system_id = msg.get_srcSystem()
#             component_id = msg.get_srcComponent()
#             print(f"✅ Heartbeat received! System: {system_id}, Component: {component_id}")
#             break
            
#     else:
#         print("❌ No heartbeat received in 10 seconds.")
        
# except Exception as e:
#     print(f"❌ Error: {e}")

# # from pymavlink import mavutil

# # master = mavutil.mavlink_connection('COM3', baud=115200)
# # master.wait_heartbeat()

# # # 请求版本信息
# # master.mav.command_long_send(
# #     master.target_system,
# #     master.target_component,
# #     mavutil.mavlink.MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES,
# #     0, 1, 0, 0, 0, 0, 0, 0
# # )

# # # 等待回复
# # msg = master.recv_match(type='AUTOPILOT_VERSION', blocking=True, timeout=5)
# # if msg:
# #     print("Firmware version:", hex(msg.flight_sw_version))
# #     print("Vendor ID:", msg.vendor_id)  # PX4 通常是 0x1234，ArduPilot 是 0xABCD

from pymavlink import mavutil

# 初始化连接
master = mavutil.mavlink_connection('COM4', baud=115200)
print("Waiting for heartbeat...")
master.wait_heartbeat()
print("Heartbeat received!")

# 请求固件版本信息
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES,
    0, 1, 0, 0, 0, 0, 0, 0
)

# 等待并接收 AUTOPILOT_VERSION 消息
msg = master.recv_match(type='AUTOPILOT_VERSION', blocking=True, timeout=5)
if msg:
    # 打印固件版本
    print("Firmware version:", hex(msg.flight_sw_version))
    # 打印厂商ID
    print("Vendor ID:", msg.vendor_id)
    # 打印产品ID
    print("Product ID:", msg.product_id)
else:
    print("Failed to receive AUTOPILOT_VERSION message.")