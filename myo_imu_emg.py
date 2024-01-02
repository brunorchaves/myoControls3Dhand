from pyomyo import Myo, emg_mode
import sys

class MyoDataPrinter:
    def __init__(self):
        self.myo = Myo(sys.argv[1] if len(sys.argv) >= 2 else None, mode=emg_mode.RAW)
        self.myo.add_imu_handler(self.on_imu)
        self.myo.add_emg_handler(self.on_emg)
        self.myo.connect()

    def on_imu(self, quat, acc, gyro):
        print('IMU Data:')
        print('Quaternion:', quat)
        print('Accelerometer:', acc)
        print('Gyroscope:', gyro)
        print()

    def on_emg(self, emg, moving):
        print('EMG Data:')
        print('EMG:', emg)
        print()

    def run(self):
        try:
            while True:
                self.myo.run()

        except KeyboardInterrupt:
            self.myo.disconnect()
            quit()

if __name__ == '__main__':
    myo_printer = MyoDataPrinter()
    myo_printer.run()

