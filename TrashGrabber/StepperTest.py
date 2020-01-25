import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
control_pins = [3, 5, 18, 22] #edit these pins
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

def clockwise90():
  for i in range(128):
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(control_pins[pin], halfstep_seq[7 - halfstep][pin])
      time.sleep(0.001)

def counter_clockwise90():
  for i in range(128):
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)

clockwise90()
counter_clockwise90()
GPIO.cleanup()


