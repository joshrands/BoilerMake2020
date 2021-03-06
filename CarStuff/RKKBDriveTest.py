# script to test driving! 

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class TwoWheel:
    def __init__(self, left_for, left_back, right_for, right_back):
        self.LEFT_FORWARD = left_for
        self.LEFT_BACKWARD = left_back
        self.RIGHT_FORWARD = right_for
        self.RIGHT_BACKWARD = right_back

        GPIO.setup(self.LEFT_FORWARD, GPIO.OUT)
        GPIO.setup(self.LEFT_BACKWARD, GPIO.OUT)
        GPIO.setup(self.RIGHT_FORWARD, GPIO.OUT)
        GPIO.setup(self.RIGHT_BACKWARD, GPIO.OUT)

    def stop(self):
        GPIO.output(self.LEFT_FORWARD, False)
        GPIO.output(self.LEFT_BACKWARD, False)
        GPIO.output(self.RIGHT_FORWARD, False)
        GPIO.output(self.RIGHT_BACKWARD, False)

    def drive_forward(self):
       # GPIO.output(self.LEFT_FORWARD, True)
       # GPIO.output(self.RIGHT_FORWARD,True)
       left =  GPIO.PWM(self.LEFT_FORWARD, 1000)
       right =  GPIO.PWM(self.RIGHT_FORWARD, 1000)
       left.start(0)
       right.start(0)
       left.ChangeDutyCycle(100)
       right.ChangeDutyCycle(100)
       time.sleep(3)
       left.stop()
       right.stop()

    def drive_backward(self):
        GPIO.output(self.LEFT_BACKWARD, True)
        GPIO.output(self.RIGHT_BACKWARD, True)

    def pivot_left(self):
        GPIO.output(self.RIGHT_FORWARD, True)
        GPIO.output(self.RIGHT_BACKWARD, False)
        GPIO.output(self.LEFT_BACKWARD, True)
        GPIO.output(self.LEFT_FORWARD, False)

    def pivot_right(self):
        GPIO.output(self.RIGHT_FORWARD, False)
        GPIO.output(self.RIGHT_BACKWARD, True)
        GPIO.output(self.LEFT_BACKWARD, False)
        GPIO.output(self.LEFT_FORWARD, True)

class FourWheel:
    def __init__(self, front, back):
        self.front_wheels = front
        self.back_wheels = back

        self.front_wheels.stop()
        self.back_wheels.stop()

    def drive_forward(self, duration, speed=25):
        self.front_wheels.drive_forward()
        self.back_wheels.drive_forward()
        time.sleep(duration)
        

    def drive_backward(self, duration, speed=25):
        self.front_wheels.drive_backward()
        self.back_wheels.drive_backward()
        time.sleep(duration)
        self.stop()
        '''
        for i in range(0, duration*25):
            self.front_wheels.drive_backward()
            self.back_wheels.drive_backward()
            time.sleep(.04 * (speed/100.0))
            self.stop()
            time.sleep(0.04 * (speed/100.0) * 3)
'''
    def pivot_left(self, duration):
        self.front_wheels.pivot_left()
        self.back_wheels.pivot_left()
        time.sleep(duration)
        self.stop()

    def pivot_right(self, duration):
        self.front_wheels.pivot_right()
        self.back_wheels.pivot_right()
        time.sleep(duration)
        self.stop()

    def stop(self):
        self.front_wheels.stop()
        self.back_wheels.stop()

back_wheels = TwoWheel(13, 11, 15, 16) #switch these on Vans thing
front_wheels = TwoWheel(37, 36, 29, 31)

drive = FourWheel(front_wheels, back_wheels)

drive.stop()
time.sleep(2)

drive.pivot_left(1)
time.sleep(3)
drive.drive_backward(1)
time.sleep(3)
drive.drive_forward(1)
time.sleep(3)
drive.pivot_right(1)

GPIO.cleanup()

