from pymavlink import mavutil

master = mavutil.mavlink_connection('COM4', baud=115200)
master.wait_heartbeat()

master.mav.my_test_msg_send(
    100,
    6.66
)

while True:
    msg = master.recv_match(type='MY_TEST_MSG', blocking=True)
    print("msg is : ", msg)
