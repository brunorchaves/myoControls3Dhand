from pyomyo import Myo, emg_mode
import sys
import math

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
        self.emg_data = []
        self.euler_angles = []
        self.myo = Myo(sys.argv[1] if len(sys.argv) >= 2 else None, mode=emg_mode.RAW)
        self.myo.add_imu_handler(self.on_imu)
        self.myo.add_emg_handler(self.on_emg)
        self.myo.set_leds([128, 0, 128], [128, 0, 128])
        self.myo.connect()

    def on_imu(self, quat, acc, gyro):
        # print('IMU Data:')
        # print('Quaternion:', quat)
        # print('Accelerometer:', acc)
        # print('Gyroscope:', gyro)
        self.euler_angles = euler_from_quaternion(quat[0], quat[1], quat[2], quat[3])
        roll, pitch, yaw = self.euler_angles
        # print('Euler Angles (in radians):')
        # print('Roll:', roll)
        # print('Pitch:', pitch)
        # print('Yaw:', yaw)
        # print()

    def on_emg(self, emg, moving):
        # print('EMG Data:')
        # print('EMG:', emg)
        self.emg_data = emg
        # print()

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
    while run_flag:
        myo_printer.run()
        emg = myo_printer.get_emg()
        euler_angles = myo_printer.get_euler_angles()
        print(emg)
        print(euler_angles)
