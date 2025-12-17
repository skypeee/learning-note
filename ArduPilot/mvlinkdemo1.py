from pymavlink import mavutil
import time

MISSION_FILE = "/home/shikun/workspace/circle_mission.txt"
TAKEOFF_ALT = 40


def send_cmd_long(master, cmd, p1=0, p2=0, p3=0, p4=0, p5=0, p6=0, p7=0):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        cmd,
        0,
        p1,p2,p3,p4,p5,p6,p7
    )


def set_mode(master, mode_id):
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id
    )


def set_guided(master):
    print("切换到 GUIDED 模式...")
    set_mode(master, 4)
    time.sleep(2)


# ============================
# 正确的 Mission 上传流程
# ============================
def upload_mission(master, mission):

    master.waypoint_clear_all_send()
    time.sleep(1)

    master.waypoint_count_send(len(mission))
    print(f"发送航点数量: {len(mission)}")

    i = 0
    while True:
        msg = master.recv_match(blocking=True)
        if msg.get_type() == "MISSION_REQUEST_INT":
            seq = msg.seq
            item = mission[seq]

            master.mav.mission_item_int_send(
                master.target_system,
                master.target_component,
                seq,
                item['frame'],
                item['command'],
                item['current'],
                item['autocontinue'],
                item['p1'], item['p2'], item['p3'], item['p4'],
                int(item['x'] * 1e7),
                int(item['y'] * 1e7),
                item['z']
            )
            print(f"发送航点 {seq}")
            i += 1

        if msg.get_type() == "MISSION_ACK":
            print("任务上传成功！")
            break


def load_mission_qgc(filename):
    with open(filename) as f:
        lines = f.readlines()

    mission = []
    for line in lines[1:]:
        if not line.strip():
            continue
        data = line.split()
        seq, current, frame, cmd, p1,p2,p3,p4,x,y,z, autoc = data

        mission.append({
            "seq": int(seq),
            "current": int(current),
            "frame": int(frame),
            "command": int(cmd),
            "p1": float(p1),
            "p2": float(p2),
            "p3": float(p3),
            "p4": float(p4),
            "x": float(x),
            "y": float(y),
            "z": float(z),
            "autocontinue": int(autoc)
        })

    return mission


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
