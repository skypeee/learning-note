from pymavlink import mavutil
import time

# ============================
# 主流程
# ============================

master = mavutil.mavlink_connection("udp:127.0.0.1:14550")
print("等待心跳...")
master.wait_heartbeat()
print("已连接 SITL")


# **关键修复：不要让任务抢占 GUIDED**
master.waypoint_set_current_send(1)
time.sleep(1)


# 2. 解锁
print("解锁中...")
send_cmd_long(master, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 1)
time.sleep(2)

# 3. 切到 GUIDED
set_guided(master)

# 4. 起飞
print(f"起飞到 {TAKEOFF_ALT} m ...")
send_cmd_long(master, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,0,0,0, 0,0, TAKEOFF_ALT)

while True:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    alt = msg.relative_alt / 1000.0
    print(f"高度: {alt:.1f} m")
    if alt >= TAKEOFF_ALT * 0.95:
        break

set_mode(master, 3)

# 1. 加载 mission
mission = load_mission_qgc(MISSION_FILE)
upload_mission(master, mission)


# 5. 自动任务
print("切 AUTO 执行任务...")
time.sleep(3)
print("任务执行中...")
