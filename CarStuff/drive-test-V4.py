import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


class carClass:
    def __init__(self, flf, flb, frf, frb, blf, blb, brf, brb):
        self.turnTime = 1
        self.FLF = flf
        self.FLB = flb
        self.FRF = frf
        self.FRB = frb
        self.BLF = blf
        self.BLB = blb
        self.BRF = brf
        self.BRB = brb

        # Pin Declarations for encoders
        self.LS = 7
        self.RS = 11

        # Encoder counts
        self.leftCount = 0
        self.rightCount = 0

        # Gain declarations and turn time for 90 degree turns
        self.fwdGain = 25
        self.turnGain = 80
        self.trackLgain = 0
        self.trackRgain = 0
        self.cmd = 0
        self.turnTime = .25

        # Pin out declarations
        GPIO.setup(self.FLF, GPIO.OUT)
        GPIO.setup(self.FLB, GPIO.OUT)
        GPIO.setup(self.FRF, GPIO.OUT)
        GPIO.setup(self.FRB, GPIO.OUT)
        GPIO.setup(self.BLF, GPIO.OUT)
        GPIO.setup(self.BLB, GPIO.OUT)
        GPIO.setup(self.BRF, GPIO.OUT)
        GPIO.setup(self.BRB, GPIO.OUT)

        # Encoder pull up set up
        GPIO.setup(self.LS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.RS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Encoder interrupt set up
        GPIO.add_event_detect(self.LS, GPIO.FALLING, callback = self.leftIterate, bouncetime = 5)
        GPIO.add_event_detect(self.RS, GPIO.FALLING, callback = self.rightIterate, bouncetime = 5)
        
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

    # Adds one to the left count
    def leftIterate(self, channel):
        self.leftCount = self.leftCount + 1
        print("Left Count: ", self.leftCount, "\n")

    # Adds one to the right count
    def rightIterate(self, channel):
        self.rightCount = self.rightCount + 1
        print("Right Count: ", self.rightCount, "\n")

    # Computes how large the gain should be based on error
    def computeCmd(self, error):
        self.cmd = error * self.fwdGain

        if self.cmd > 100:
            self.cmd = 100

        elif self.cmd < 40:
            self.cmd = 40

        return self.cmd

    # Computes gain based on where object is in frame
    def computeTrackCmd(self, error):
        # Positive error mean person is to the right of the center of the screen -> L is greater than R
        # Negative error mean person is to the left of the center of the screen -> R is greater than L

        pwmBase = 75 #Base PWM Value
        errorScale = 25 #Modifiable based on base PWM
        self.trackLgain = pwmBase + (error*errorScale) #Gets bigger if object is on the right of screen
        self.trackRgain = pwmBase - (error*errorScale) #Gets bigger if object is on the left of screen


# Start of code to make ultrasonic work
trigPin = 8
echoPin = 10

GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

def distUltra():
    GPIO.output(trigPin, True)

    time.sleep(0.00001)
    GPIO.output(trigPin, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(echoPin) == 0:
        StartTime = time.time()

    while GPIO.input(echoPin) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2 #in cm

    return distance

######################## Start of Main #########################

#Creating a car object using the following 8 pins
car = carClass(37, 35, 31, 33, 40, 38, 16, 18)

goalTravelFt = 5 #Travel goal in feet
goalTravelIn = goalTravelFt * 12 #Convert to inches
InchPerCt = 4.125 #Inches car moves per encoder count
stopDistance = 50 #cm #Limit that will cause car to stop if ultrasonic gets too close to object

CountsDes = goalTravelIn/InchPerCt # Find amount of times the wheels need to turn
Lerror = CountsDes - car.leftCount # left error
Rerror = CountsDes - car.rightCount # right error
avgError = (Lerror + Rerror)/2 # average the errors

loopCount = 0
lastLerr = Lerror
lastRerr = Rerror

time.sleep(.5)

while (avgError > 0):
    car.forward(car.computeCmd(avgError)) # Calculate the forward gain and drive forward at that speed

    # If the ultrasonic distance is less than the threshold, the car stops
    while (distUltra() < stopDistance):
        car.stop()

    # Recalculate error
    Lerror = CountsDes - car.leftCount
    Rerror = CountsDes - car.rightCount

    # Reset the loop counts if either of the errors are different
    if Lerror != lastLerr
        loopCount = 0
    elif Rerror != lastRerr
        loopCount = 0

    # Recalc average and iterate loop count
    avgError = (Lerror + Rerror) / 2
    loopCount += 1
    time.sleep(.010)

    # If the loop count is greater than 50 break so seg fault does not happen
    if loopCount > 50
        break

car.stop() #Stop car at the end





