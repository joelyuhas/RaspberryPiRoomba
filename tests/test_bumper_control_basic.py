"""
Joel Yuhas
April 2024

Bumper Control Test Basic
-------------------------

Very basic bumper control test, doesn't use the class and simply prints out if the bumper is being activated or not.
Useful for verifying class changes as well as hardware changes.

"""
import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the BCM GPIO channel connected to your bumper sensor
bumper_pin1 = 16  # Replace with the actual BCM GPIO channel number you're using
bumper_pin2 = 26  # Replace with the actual BCM GPIO channel number you're using

# Set up the GPIO pin for input
GPIO.setup(bumper_pin1, GPIO.IN)
GPIO.setup(bumper_pin2, GPIO.IN)

try:
    while True:
        # Read the state of the bumper sensor
        bumper_state1 = GPIO.input(bumper_pin1)
        bumper_state2 = GPIO.input(bumper_pin2)

        # Check if bumper is pressed
        if bumper_state1 == GPIO.LOW:
            print("PRESSED 1")
        else:
            print("NOT PRESSED 1")

        print(f"HERE {bumper_state1} {bumper_state2}")

        # Check if bumper is pressed
        if bumper_state2 == GPIO.LOW:
            print("PRESSED 2")
        else:
            print("NOT PRESSED 2")
        time.sleep(0.5)


except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()