import smbus
import time
import json
import requests
import os

class Dryer:
  dryer_state = "unknown"
  previous_dryer_state = "unknown"
  transition_time = 0
  notification_sent = False 

  def dryer_off(self,transition_time):
    current_time = time.time()
    if current_time > transition_time + 60:
      time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(transition_time))
      if self.notification_sent == False and self.previous_dryer_state == "on" :
        self.send_notification()
        self.notification_sent = True

  def dryer_on(self, transition_time):
    self.notification_sent = False

  def send_notification(self):
    print("sending notification")
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    slack_data = {'text' : 'Dryer stopped'}
    response = requests.post(slack_webhook_url, json=slack_data)
    if response.status_code != 200:
        print(f'Slack returned an error: {response.status_code} {response.text}')

  def set_state(self, state):
    self.previous_dryer_state = self.dryer_state
    self.dryer_state = state

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

def push_average_array(arr, element):
  arr.append(element)
  if len(arr) > 5:
    arr.pop(1)
  return sum(arr) / len(arr)

if __name__ == '__main__':
  bus = smbus.SMBus(1)
  init_imu(bus)
  last_reading = 0
  readings_list = []
  readings = 0

  dryer = Dryer()
  while True:
    readings += 1
    reading = get_reading(bus)
    x_diff = abs(reading - last_reading)
    readings_average = push_average_array(readings_list, x_diff)
    if readings > 5:
      print(f'{readings} {readings_average}')
      if readings_average > 100:
        if dryer.dryer_state != "on":
          transition_time = time.time()
          dryer.set_state("on")
        dryer.dryer_on(transition_time)
      else:
        if dryer.dryer_state != "off":
          transition_time = time.time()
          dryer.set_state("off")
        dryer.dryer_off(transition_time)
    last_reading = reading
    time.sleep(1)
