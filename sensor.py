import smbus
import time
from icm20948 import ICM20948
from dryer import Dryer

if __name__ == '__main__':
  icm20948 = ICM20948()
 

  dryer = Dryer()
  while True:
    ax, ay, az, gx, gy, gz = icm20948.read_accelerometer_gyro_data()
    mx, my, mz = icm20948.read_magnetometer_data()
    t = int(time.time())
    print(f'{t} {ax} {ay} {az} {gx} {gy} {gz} {mx} {my} {mz}')
    dryer.add_reading(ax, ay, az, gx, gy, gz, mx, my, mz)
    time.sleep(1)
