from dryer import Dryer
import time

dryer = Dryer()

with open('test-data.txt') as file:
  for line in file:
    chunks=line.split(' ')
    if chunks[1] == "A":
      dryer.add_reading(int(chunks[2]))
      time.sleep(1)
      
