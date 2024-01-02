from pyomyo import Myo, emg_mode
import sys
import math
import socket

host, port = "127.0.0.1", 25001
TEST_MODE = True


class MyoDataPrinter:
    def __init__(self):
        self.emg_data = [None] * 8
        self.euler_angles = [0.0, 0.0, 0.0]
        self.myo = Myo(mode=emg_mode.RAW)
        self.myo.add_imu_handler(self.on_imu)
        self.myo.add_emg_handler(self.on_emg)
        self.myo.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs
        self.myo.connect()

    def on_imu(self, quat, acc, gyro):
        self.euler_angles = euler_from_quaternion(quat[0], quat[1], quat[2], quat[3])

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

def euler_from_quaternion(w, x, y, z):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    roll_x = int((roll_x)*(180/math.pi))
    
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    pitch_y = int((pitch_y)*(180/math.pi))


    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    yaw_z = int((yaw_z)*(180/math.pi))

    return roll_x, pitch_y, yaw_z  # in radians

if __name__ == '__main__':
    myo_printer = MyoDataPrinter()
    yaw, pitch, roll = 1.0, 2.0, 3.0
    control_value = 1

    # SOCK_STREAM means TCP socket
    if(TEST_MODE == False):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server and send the data
        if(TEST_MODE == False):
            sock.connect((host, port))
        else:
            print("Test mode on")

        while True:
            myo_printer.run()
            emg = myo_printer.get_emg()
            euler_angles = myo_printer.get_euler_angles()

            if None not in emg[:7] and None not in euler_angles:
                emg_float = [float(element) for element in emg]
                yaw, pitch, roll = euler_angles
                # data = f"{control_value},{yaw},{pitch},{roll}"
                data = f"{yaw},{pitch},{roll}"
                print(emg_float)
                print(euler_angles)
                if(TEST_MODE == False):
                    sock.sendall(data.encode("utf-8"))
                    response = sock.recv(1024).decode("utf-8")
                    print(response)

    except KeyboardInterrupt:
        print("Exiting loop.")
    finally:
        if(TEST_MODE == False):
            sock.close()
        else:
            print("Test mode on")
