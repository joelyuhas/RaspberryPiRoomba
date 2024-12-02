"""
Joel Yuhas
April 2024

Primary program to run the "main" roomba execution. This program will take all updated code and continually execute
on the roomba.

"""
import threading

from libraries.RoombaMotion import RoombaMotion
from libraries.ControllerManager import ControllerManager
from libraries.RoombaBumper import RoombaBumper
from libraries.GPIOManager import GPIOManager
from libraries.AudioManager import AudioManager


# Attempt to initialize the primary classes
gpio_manager = GPIOManager()
audio_manager = AudioManager()
controller_manager = ControllerManager()


# Primary Try/Except block with cleanup
try:
    # Create the RoombaMotion class with correct controller and GPIO
    roomba_motion = RoombaMotion(gpio_controller=gpio_manager, xbox_controller=controller_manager)

    # Instantiate and initialize bumper control with correct GPIO
    bumper_control = RoombaBumper(gpio_controller=gpio_manager, audio_controller=audio_manager)

    # Create and start the threading for the controller and bumper
    controller_thread = threading.Thread(target=roomba_motion.motion_thread)
    bumper_thread = threading.Thread(target=bumper_control.bumper_thread)

    # Start and wait for threads to finish
    controller_thread.start()
    bumper_thread.start()

    controller_thread.join()
    bumper_thread.join()

except KeyboardInterrupt:
    gpio_manager.cleanup()
