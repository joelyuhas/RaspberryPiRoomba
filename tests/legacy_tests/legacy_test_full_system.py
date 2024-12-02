"""

Previous legacy method for testing all aspects together. This method was primarily used for rapid prototyping and
doesn't use any classes. Keeping in the legacy_test section so it can be compared and contrasted to.

"""
import RPi.GPIO as GPIO
import time


import evdev
from evdev import InputDevice, categorize, ecodes

import pygame.mixer
import random
import threading


# put all the intialization stuff into a building blocsk clas too
# initialization section
pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.mixer.init()  # turn all of pygame on.
AUDIO_DIRECTORY = "/home/pi/git/raspberrypi-items/roomba/audio/"

audio_file_list = [AUDIO_DIRECTORY + "1.wav",
                   AUDIO_DIRECTORY + "2.wav",
                   AUDIO_DIRECTORY + "3.wav",
                   AUDIO_DIRECTORY + "4.wav",
                   AUDIO_DIRECTORY + "5.wav",
                   AUDIO_DIRECTORY + "6.wav"]


# Find the Xbox controller device
devices = [InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    if "Xbox" in device.name:
        xbox_controller = device
        break
else:
    raise IOError("Xbox controller not found")

print("Using Xbox controller:", xbox_controller.name)




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



# set bumper controls
bumper_pin1 = 16  # Replace with the actual BCM GPIO channel number you're using
bumper_pin2 = 26  # Replace with the actual BCM GPIO channel number you're using

# Set up the GPIO pin for input
GPIO.setup(bumper_pin1, GPIO.IN)
GPIO.setup(bumper_pin2, GPIO.IN)



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


DEAD_ZONE_MIDDLE = 32767
DEAD_ZONE_AMOUNT = 7500
DEAD_ZONE_LOWER = DEAD_ZONE_MIDDLE - DEAD_ZONE_AMOUNT
DEAD_ZONE_UPPER = DEAD_ZONE_MIDDLE + DEAD_ZONE_AMOUNT
DEAD_ZONE_RANGE = DEAD_ZONE_LOWER
DEAD_ZONE_MAX = 65535

x_axis_value = 0
y_axis_value = 0

PREV_DIRECTION = FORWARD


# eventually, put all of this into a building blocks class
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

# Function to set motor speed
def set_motor_speed(speed):
    pwm1.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)

def set_left_motor_speed(speed):
    pwm1.ChangeDutyCycle(speed)

def set_right_motor_speed(speed):
    pwm2.ChangeDutyCycle(speed)



def set_balance(x_value, desired_speed):
    absolute_value = x_value - DEAD_ZONE_MIDDLE
    percentage = (absolute_value / DEAD_ZONE_MIDDLE)

    # invert the percentage since the closer to the center the faster the oppisite wheel we want it to go
    invert_percentage = 1 - abs(percentage)

    # if negative, turning left since negative of middle of 65535
    if percentage < 0:
        set_left_motor_speed(desired_speed)
        set_right_motor_speed(int(desired_speed * invert_percentage))

    # turning right:
    else:
        set_right_motor_speed(desired_speed)
        set_left_motor_speed(int(desired_speed * invert_percentage))


def get_turning_speed(x_value):
    absolute_value = x_value - DEAD_ZONE_MIDDLE

    return_value = int(abs((absolute_value / DEAD_ZONE_MIDDLE) * 100))
    if return_value >= 100:
        return 100

    return return_value



def get_speed(y_value):
    absolute_value = y_value - DEAD_ZONE_MIDDLE

    # if negative, send it backwards
    if absolute_value < 0:
        set_motor_direction(FORWARD)


    # sending forawrds
    else:
        set_motor_direction(BACKWARD)


    return int(abs((absolute_value / DEAD_ZONE_MIDDLE) * 100))




def controller_thread():
    x_axis_value = 0
    y_axis_value = 0

    for event in xbox_controller.read_loop():
        if event.type == ecodes.EV_ABS:  # Analog input (joysticks and triggers)
            absevent = categorize(event)
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                x_axis_value = absevent.event.value

            elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                y_axis_value = absevent.event.value

            # if in dead zone, set to 0
            if DEAD_ZONE_LOWER < x_axis_value < DEAD_ZONE_UPPER and DEAD_ZONE_LOWER < y_axis_value < DEAD_ZONE_UPPER:
                set_motor_direction(STOP)

            # if Y in dead zone, but X to the right, perform right turn
            elif 65536 > x_axis_value > DEAD_ZONE_UPPER > y_axis_value > DEAD_ZONE_LOWER:
                p = get_turning_speed(x_axis_value)
                set_motor_speed(p)
                # If the direction was previously going backward, invert the turn (makes sense when doing backwards
                # turns)
                if PREV_DIRECTION == FORWARD:
                    set_motor_direction(RIGHT)
                else:
                    set_motor_direction(LEFT)

            # if Y in dead zone, but X to the left, perform left turn
            elif 0 <= x_axis_value < DEAD_ZONE_LOWER < y_axis_value < DEAD_ZONE_UPPER:
                p = get_turning_speed(x_axis_value)
                set_motor_speed(p)
                # If the direction was previously going backward, invert the turn (makes sense when doing backwards
                # turns)
                if PREV_DIRECTION == FORWARD:
                    set_motor_direction(LEFT)
                else:
                    set_motor_direction(RIGHT)

            else:
                percentage = get_speed(y_axis_value)
                set_balance(x_axis_value, percentage)

            # If Y is up, go forward and balance based on X location
            # if DEAD_ZONE_LOWER < y_axis_value < 65536:

            # Add more conditions for other analog inputs as needed
        elif event.type == ecodes.EV_KEY:  # Digital input (buttons)
            if event.value == 1:  # Button pressed
                print("Button pressed:", event.code)
            elif event.value == 0:  # Button released
                print("Button released:", event.code)
            # Add more conditions for other buttons as needed


def gpio_thread():
    while True:
        time.sleep(0.1)
        bumper_state1 = GPIO.input(bumper_pin1)
        bumper_state2 = GPIO.input(bumper_pin2)

        if bumper_state1 == 0 or bumper_state2 == 0:
            random_number = random.randint(1, 6)
            sound = pygame.mixer.Sound(audio_file_list[random_number - 1])
            sound.play()
            time.sleep(sound.get_length())

        pass



# Example usage
try:
    controller_thread = threading.Thread(target=controller_thread)
    gpio_thread = threading.Thread(target=gpio_thread)

    controller_thread.start()
    gpio_thread.start()

    controller_thread.join()
    gpio_thread.join()




except KeyboardInterrupt:
    pwm1.stop() # Stop PWM
    pwm2.stop() # Stop PWM
    GPIO.cleanup() # Clean up GPIO pins
