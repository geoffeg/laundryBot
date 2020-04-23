import sys
import time
import json
import requests
import os
import psycopg2
from collections import deque
from statistics import variance

class Dryer:
  dryer_state = "unknown"
  previous_dryer_state = "unknown"
  transition_time = 0
  state_time = 0
  notification_sent = False 
  readings = deque(maxlen=10)
  poll_interval = 60 # seconds
  last_db_insert_time = 0

  def __init__(self):
    self.state_time = time.time()

  def write_readings(self, ax, ay, az, mx, my, mz, gx, gy, gz):
    sensor_name_map = {
      'accelerometer_x' : ax,
      'accelerometer_y' : ay,
      'accelerometer_z' : az,
      'magnetometer_x'  : mx,
      'magnetometer_y'  : my,
      'magnetometer_z'  : mz,
      'gyroscope_x'     : gx,
      'gyroscope_y'     : gy,
      'gyroscope_z'     : gz
    }

    if (self.dryer_state == "off" and time.time() > self.last_db_insert_time + 60) or self.dryer_state == "on":
      self.last_db_insert_time = time.time()
   
      attempts = 0
      while attempts < 3:
        try:
          if not hasattr(self, 'db') or self.db is None:
            self.db = psycopg2.connect("dbname=sensors host=192.168.86.186 port=6543")
          cursor = self.db.cursor()
          insert = cursor.executemany("INSERT into readings (device_id, sensor_id, reading) VALUES((SELECT id from devices where name = 'dryer'), (SELECT id from sensors where name = %s), %s)", list(sensor_name_map.items()))
          self.db.commit()
          break
        except Exception as e:
         attempts += 1
         print(e)

  def dryer_off(self):
    current_time = time.time()
    if current_time > self.transition_time + 60:
      time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.transition_time))
      if self.notification_sent == False and self.previous_dryer_state == "on" and self.state_time > 600 :
        self.poll_interval = 60
        self.send_notification()
        self.notification_sent = True

  def dryer_on(self):
    self.poll_interval = 60
    self.notification_sent = False

  def send_notification(self):
    print("sending notification")
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    slack_data = {'text' : 'Dryer finished'}
    response = requests.post(slack_webhook_url, json=slack_data)
    if response.status_code != 200:
        print(f'Slack returned an error: {response.status_code} {response.text}')

  def set_state(self, state):
    self.previous_dryer_state = self.dryer_state
    self.dryer_state = state

  def transition(self):
    print(f'transition from {self.dryer_state}')
    self.state_time = time.time() - self.transition_time
    self.transition_time = time.time()

  def add_reading(self, ax, ay, az, gx, gy, gz, mx, my, mz):
    ax = ax * 1000
    self.readings.append(ax)
    self.write_readings(ax, ay, az, gx, gy, gz, mx, my, mz)
    if len(self.readings) == 10:
      readings_variance = int(variance(self.readings))
      print(f'{ax} {readings_variance}')
      if readings_variance > 500:
        if self.dryer_state != "on":
          self.transition()
          self.set_state("on")
        self.dryer_on()
      else:
        if self.dryer_state != "off":
          self.transition()
          self.set_state("off")
        self.dryer_off()
    else:
      print(ax)
