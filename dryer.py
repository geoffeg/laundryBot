import time
import json
import requests
import os
from collections import deque
from statistics import variance

class Dryer:
  dryer_state = "unknown"
  previous_dryer_state = "unknown"
  transition_time = 0
  state_time = 0
  notification_sent = False 
  readings = deque(maxlen=15)

  def dryer_off(self):
    current_time = time.time()
    if current_time > self.transition_time + 60:
      time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.transition_time))
      if self.notification_sent == False and self.previous_dryer_state == "on" and self.state_time > 600 :
        self.send_notification()
        self.notification_sent = True

  def dryer_on(self):
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

  def transition(self):
    self.state_time = time.time() - self.transition_time
    self.transition_time = time.time()

  def add_reading(self, reading):
    self.readings.append(reading)
    if len(self.readings) == 15:
      readings_variance = int(variance(self.readings))
      print(f'{reading} {readings_variance}')
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
      print(reading)
