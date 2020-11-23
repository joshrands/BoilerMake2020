import RPi.GPIO as GPIO
import time
import socket
import pickle

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class carClass:
    def __init__(self, flf, flb, frf, frb, blf, blb, brf, brb):
        # Define motor pins
        self.FLF = flf
        self.FLB = flb
        self.FRF = frf
        self.FRB = frb
        self.BLF = blf
        self.BLB = blb
        self.BRF = brf
        self.BRB = brb

        # Gain declarations and turn time for 90 degree turns
        self.turnGain = 80
        self.turnTime = 1 

        # Pin out declarations
        GPIO.setup(self.FLF, GPIO.OUT)
        GPIO.setup(self.FLB, GPIO.OUT)
        GPIO.setup(self.FRF, GPIO.OUT)
        GPIO.setup(self.FRB, GPIO.OUT)
        GPIO.setup(self.BLF, GPIO.OUT)
        GPIO.setup(self.BLB, GPIO.OUT)
        GPIO.setup(self.BRF, GPIO.OUT)
        GPIO.setup(self.BRB, GPIO.OUT)

        # Setting the frequency of the PWM
        self.FLF_PWM = GPIO.PWM(self.FLF, 1000)
        self.FLB_PWM = GPIO.PWM(self.FLB, 1000)
        self.FRF_PWM = GPIO.PWM(self.FRF, 1000)
        self.FRB_PWM = GPIO.PWM(self.FRB, 1000)
        self.BLF_PWM = GPIO.PWM(self.BLF, 1000)
        self.BLB_PWM = GPIO.PWM(self.BLB, 1000)
        self.BRF_PWM = GPIO.PWM(self.BRF, 1000)
        self.BRB_PWM = GPIO.PWM(self.BRB, 1000)

        # Setting all PWM initial outputs to a duty cycle of 0
        self.FLF_PWM.start(0)
        self.FLB_PWM.start(0)
        self.FRF_PWM.start(0)
        self.FRB_PWM.start(0)
        self.BLF_PWM.start(0)
        self.BLB_PWM.start(0)
        self.BRF_PWM.start(0)
        self.BRB_PWM.start(0)

        self.right_pwm = 0
        self.left_pwm = 0
        self.step_size = 10

    def driveMotors(self):
        if (self.right_pwm > 100):
            self.right_pwm = 100
        elif (self.right_pwm < -100):
            self.right_pwm = -100

        if (self.left_pwm > 100):
            self.left_pwm = 100
        elif (self.left_pwm < -100):
            self.left_pwm = -100
        
        if (self.right_pwm >= 0):
            self.FRF_PWM.ChangeDutyCycle(self.right_pwm)
            self.BRF_PWM.ChangeDutyCycle(self.right_pwm)
            self.FRB_PWM.ChangeDutyCycle(0)
            self.BRB_PWM.ChangeDutyCycle(0)
        else: 
            self.FRF_PWM.ChangeDutyCycle(0)
            self.BRF_PWM.ChangeDutyCycle(0)
            self.FRB_PWM.ChangeDutyCycle(-1*self.right_pwm)
            self.BRB_PWM.ChangeDutyCycle(-1*self.right_pwm)

        if (self.left_pwm >= 0):
            self.FLF_PWM.ChangeDutyCycle(self.left_pwm)
            self.BLF_PWM.ChangeDutyCycle(self.left_pwm)
            self.FLB_PWM.ChangeDutyCycle(0)
            self.BLB_PWM.ChangeDutyCycle(0)
        else:
            self.FLF_PWM.ChangeDutyCycle(0)
            self.BLF_PWM.ChangeDutyCycle(0)
            self.FLB_PWM.ChangeDutyCycle(-1*self.left_pwm)
            self.BLB_PWM.ChangeDutyCycle(-1*self.left_pwm)

    def stepForward(self):
        if (self.right_pwm == 0):
            self.right_pwm = 30
            self.left_pwm = 30
        else:
            self.right_pwm += self.step_size
            self.left_pwm += self.step_size

        self.driveMotors()

    def stepBackward(self):
        if (self.right_pwm == 0):
            self.right_pwm = -30 
            self.left_pwm = -30 
        else: 
            self.right_pwm -= self.step_size
            self.left_pwm -= self.step_size

        self.driveMotors()

    def stepRight(self):
        self.right_pwm = -60 
        self.left_pwm = 60 
        self.driveMotors()
        time.sleep(0.2)
        self.right_pwm = 0 
        self.left_pwm = 0 
        self.driveMotors()

    def stepLeft(self):
        self.left_pwm = -60 
        self.right_pwm = 60 
        self.driveMotors()
        time.sleep(0.2)
        self.left_pwm = 0 
        self.right_pwm = 0 
        self.driveMotors()

    # Stops all PWM permanently
    def end(self):
        self.FLF_PWM.stop()
        self.FLB_PWM.stop()
        self.FRF_PWM.stop()
        self.FRB_PWM.stop()
        self.BLF_PWM.stop()
        self.BLB_PWM.stop()
        self.BRF_PWM.stop()
        self.BRB_PWM.stop()

    # Turns all motors off
    def stop(self):
        self.FLF_PWM.ChangeDutyCycle(0)
        self.FLB_PWM.ChangeDutyCycle(0)
        self.FRF_PWM.ChangeDutyCycle(0)
        self.FRB_PWM.ChangeDutyCycle(0)
        self.BLF_PWM.ChangeDutyCycle(0)
        self.BLB_PWM.ChangeDutyCycle(0)
        self.BRF_PWM.ChangeDutyCycle(0)
        self.BRB_PWM.ChangeDutyCycle(0)

    # Forward function with duty cycle as input
    def forward(self, duty_cycle):
        self.FLF_PWM.ChangeDutyCycle(duty_cycle)
        self.FLB_PWM.ChangeDutyCycle(0)
        self.FRF_PWM.ChangeDutyCycle(duty_cycle)
        self.FRB_PWM.ChangeDutyCycle(0)
        self.BLF_PWM.ChangeDutyCycle(duty_cycle)
        self.BLB_PWM.ChangeDutyCycle(0)
        self.BRF_PWM.ChangeDutyCycle(duty_cycle)
        self.BRB_PWM.ChangeDutyCycle(0)

    # Backward function with duty cycle as input
    def backward(self, duty_cycle):
        self.FLF_PWM.ChangeDutyCycle(0)
        self.FLB_PWM.ChangeDutyCycle(duty_cycle)
        self.FRF_PWM.ChangeDutyCycle(0)
        self.FRB_PWM.ChangeDutyCycle(duty_cycle)
        self.BLF_PWM.ChangeDutyCycle(0)
        self.BLB_PWM.ChangeDutyCycle(duty_cycle)
        self.BRF_PWM.ChangeDutyCycle(0)
        self.BRB_PWM.ChangeDutyCycle(duty_cycle)

    # Left turn function
    def left_turn(self):
        self.FLF_PWM.ChangeDutyCycle(0)
        self.FLB_PWM.ChangeDutyCycle(self.turnGain)
        self.FRF_PWM.ChangeDutyCycle(self.turnGain)
        self.FRB_PWM.ChangeDutyCycle(0)
        self.BLF_PWM.ChangeDutyCycle(0)
        self.BLB_PWM.ChangeDutyCycle(self.turnGain)
        self.BRF_PWM.ChangeDutyCycle(self.turnGain)
        self.BRB_PWM.ChangeDutyCycle(0)
        time.sleep(self.turnTime)

    # Right turn function
    def right_turn(self):
        self.FLF_PWM.ChangeDutyCycle(self.turnGain)
        self.FLB_PWM.ChangeDutyCycle(0)
        self.FRF_PWM.ChangeDutyCycle(0)
        self.FRB_PWM.ChangeDutyCycle(self.turnGain)
        self.BLF_PWM.ChangeDutyCycle(self.turnGain)
        self.BLB_PWM.ChangeDutyCycle(0)
        self.BRF_PWM.ChangeDutyCycle(0)
        self.BRB_PWM.ChangeDutyCycle(self.turnGain)
        time.sleep(self.turnTime)

    # Function for navigating to an object in frame
    def track_turn(self):
        self.FLF_PWM.ChangeDutyCycle(self.trackLgain)
        self.FLB_PWM.ChangeDutyCycle(0)
        self.FRF_PWM.ChangeDutyCycle(self.trackRgain)
        self.FRB_PWM.ChangeDutyCycle(0)
        self.BLF_PWM.ChangeDutyCycle(self.trackLgain)
        self.BLB_PWM.ChangeDutyCycle(0)
        self.BRF_PWM.ChangeDutyCycle(self.trackRgain)
        self.BRB_PWM.ChangeDutyCycle(0)


######################## Start of Main #########################

#Creating a car object using the following 8 pins
#myCar = carClass(37, 35, 31, 33, 40, 38, 16, 18)
#myCar = carClass(37, 36, 29, 31, 13, 11, 15, 16)

#myCar.left_turn()
#time.sleep(1)
#myCar.right_turn()

#myCar.stop()

