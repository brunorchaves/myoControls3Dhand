from pyomyo import Myo, emg_mode
import sys
import math
import socket

# host, port = "127.0.0.1", 25001
# data = "1,2,3"

# # SOCK_STREAM means TCP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     # Connect to the server and send the data
#     sock.connect((host, port))
#     sock.sendall(data.encode("utf-8"))
#     response = sock.recv(1024).decode("utf-8")
#     print (response)

# finally:
#     sock.close()



def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z  # in radians


class MyoDataPrinter:
    def __init__(self):
        self.emg_data = [None] * 8
        self.euler_angles = []
        self.myo = Myo(mode=emg_mode.RAW)
        self.myo.add_imu_handler(self.on_imu)
        self.myo.add_emg_handler(self.on_emg)
        self.myo.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs
        self.myo.connect()

    def on_imu(self, quat, acc, gyro):
        # print('IMU Data:')
        # print('Quaternion:', quat)
        # print('Accelerometer:', acc)
        # print('Gyroscope:', gyro)
        self.euler_angles = euler_from_quaternion(quat[0], quat[1], quat[2], quat[3])
        roll, pitch, yaw = list(self.euler_angles)
        # print('Euler Angles (in radians):')
        # print('Roll:', roll)
        # print('Pitch:', pitch)
        # print('Yaw:', yaw)
        # print()

    def on_emg(self, emg, moving):
        self.emg_data = list(emg)
        

    def get_emg(self):
        return self.emg_data

    def get_euler_angles(self):
        return self.euler_angles

    def run(self):
        try:
            self.myo.run()

        except KeyboardInterrupt:
            self.myo.disconnect()
            quit()

if __name__ == '__main__':
    myo_printer = MyoDataPrinter()
    run_flag = True
    printDivider = 5
    while run_flag:
        myo_printer.run()
        emg = myo_printer.get_emg()
        euler_angles = myo_printer.get_euler_angles()
        # print(str(emg[6])+ str(emg[7]))
        # print(euler_angles)
        # Take the absolute value of each element in the list
        if None not in emg[:7]:
            emg_float = [float(element) for element in emg]
            print(emg_float)
        if None not in euler_angles[:2]:
            euler_angles_float = [float(element) for element in euler_angles]
            print(euler_angles_float)
            

            

            
