import smbus
import time
from dryer import Dryer

def init_imu(bus):
  bus.write_byte_data(0x68, 0x7F, 0x00) # Select bank 0
  bus.write_byte_data(0x68, 0x06, 0x80) # Reset
  time.sleep(0.1)
  bus.write_byte_data(0x68, 0x06, 0x01) # Run mode
  bus.write_byte_data(0x68, 0x7F, 0x20) # Select bank 2
  bus.write_byte_data(0x68, 0x14, 0x30 | 0x00 | 0x01) # 2g modee
  bus.write_byte_data(0x68, 0x7F, 0x00) # Select bank 0

def get_reading(bus):
  x_high = bus.read_byte_data(0x68, 0x2D)
  x_low = bus.read_byte_data(0x68, 0x2E)
  x = (x_high<<8)|x_low
  if x>=32767:
    x=x-65535
  elif x<=-32767:
    x=x+65535
  return x

if __name__ == '__main__':
  bus = smbus.SMBus(1)
  init_imu(bus)

  dryer = Dryer()
  while True:
    reading = get_reading(bus)
    dryer.add_reading(reading)
    time.sleep(1)
