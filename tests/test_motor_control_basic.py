"""
Joel Yuhas
April 2024

Basic Motor Test
----------------------

Very basic motor test. Doesn't use classes and directly instantiates everything (GPIO). This is to do a sanity check to
ensure  that if there is an issue, changes to the classes can be ruled out. Also doesn't involve the Audio or Controller
to minimize potential issues.

Bare-bones check to ensure that the raspberry pi can still control the motors without any overhead or anything else.

Often when doing hardware changes, this test is used to very quickly verify any changes and updates.

The "basic" refers to the fact that this test does not use any of the classes and instantiates everything on its own.

"""
import RPi.GPIO as GPIO
import time

# setup the pins here
# Define GPIO pins
enable1_pin = 18
enable2_pin = 12
input1_pin = 23
input2_pin = 24
input3_pin = 17
input4_pin = 27
input5_pin = 22 # left bumper sensor
input6_pin = 25 # right bumper sensor


# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(enable1_pin, GPIO.OUT)
GPIO.setup(enable2_pin, GPIO.OUT)
GPIO.setup(input1_pin, GPIO.OUT)
GPIO.setup(input2_pin, GPIO.OUT)
GPIO.setup(input3_pin, GPIO.OUT)
GPIO.setup(input4_pin, GPIO.OUT)

GPIO.setup(input5_pin, GPIO.IN)
GPIO.setup(input6_pin, GPIO.IN)

# Set PWM for speed control
pwm1 = GPIO.PWM(enable1_pin, 100)
pwm2 = GPIO.PWM(enable2_pin, 100)
pwm1.start(50) # Start PWM with duty cycle 0
pwm2.start(50) # Start PWM with duty cycle 0

# Function to set motor direction


FORWARD = 0
BACKWARD = 1
LEFT = 2
RIGHT = 3
STOP = 4


def left_wheel(direction):
    if direction == FORWARD:
        GPIO.output(input1_pin, GPIO.HIGH)
        GPIO.output(input2_pin, GPIO.LOW)
    elif direction == BACKWARD:
        GPIO.output(input1_pin, GPIO.LOW)
        GPIO.output(input2_pin, GPIO.HIGH)
    elif direction == STOP:
        GPIO.output(input1_pin, GPIO.LOW)
        GPIO.output(input2_pin, GPIO.LOW)


def right_wheel(direction):
    if direction == BACKWARD:
        GPIO.output(input3_pin, GPIO.HIGH)
        GPIO.output(input4_pin, GPIO.LOW)
    elif direction == FORWARD:
        GPIO.output(input3_pin, GPIO.LOW)
        GPIO.output(input4_pin, GPIO.HIGH)
    elif direction == STOP:
        GPIO.output(input3_pin, GPIO.LOW)
        GPIO.output(input4_pin, GPIO.LOW)


def set_motor_speed(speed):
    pwm1.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)


def set_left_motor_speed(speed):
    pwm1.ChangeDutyCycle(speed)


def set_right_motor_speed(speed):
    pwm2.ChangeDutyCycle(speed)


def set_motor_direction(direction):
    if direction == BACKWARD or direction == FORWARD or direction == STOP:
        left_wheel(direction)
        right_wheel(direction)
    elif direction == RIGHT:
        left_wheel(BACKWARD)
        right_wheel(FORWARD)
    elif direction == LEFT:
        left_wheel(FORWARD)
        right_wheel(BACKWARD)
    else:
        GPIO.output(input1_pin, GPIO.LOW)
        GPIO.output(input2_pin, GPIO.LOW)
        GPIO.output(input3_pin, GPIO.LOW)
        GPIO.output(input4_pin, GPIO.LOW)


# Primary test steps.
set_motor_speed(75)  # Set motor speed (0-100)
time.sleep(2)
set_motor_speed(0)  # Stop motor
set_motor_direction('forward')  # Set motor direction (options: forward, backward)
set_motor_speed(50)             # Set motor speed (0-100)
time.sleep(2)
set_motor_speed(0)              # Stop motor
time.sleep(1)
set_motor_direction('backward')
set_motor_speed(25)
time.sleep(2)
set_motor_speed(0)
time.sleep(1)

