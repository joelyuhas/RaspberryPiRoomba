"""
Joel Yuhas
April 2024

Primary area for managing and controlling the bumper sensors on the roomba.

"""
import RPi.GPIO as GPIO
import time

from GPIOManager import GPIOManager
from AudioManager import AudioManager


class RoombaBumper:
    """
    The primary class used for organizing and performing the logic that should happen when the bumper on the roomba
    detects a collision. Checks the bumper status and then performs some action.

    """
    # the GPIO bumper pins being used to read the bumper outputs
    SLEEP_BETWEEN_LOOPS_SECONDS = 0.1

    def __init__(self, gpio_controller: GPIOManager, audio_controller: AudioManager):
        self.gpio_controller = gpio_controller
        self.audio_controller = audio_controller

    def bumper_thread(self):
        """
        Primary thread used to run the bumper logic. Specifically, when one of the bumpers is hit, what actions to
        perform.

        Currently setup to play a random sound every time the bumper detects a hit.

        """
        while True:
            time.sleep(self.SLEEP_BETWEEN_LOOPS_SECONDS)
            bumper_state1 = GPIO.input(self.gpio_controller.BUMPER_PIN_1)
            bumper_state2 = GPIO.input(self.gpio_controller.BUMPER_PIN_2)

            if bumper_state1 == 0 or bumper_state2 == 0:
                self.audio_controller.play_random_sound()
