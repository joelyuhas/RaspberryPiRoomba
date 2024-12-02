"""
Joel Yuhas
April 2024

RoombaBumper Test
-------------------------

Test for verifying the RoombaBumper class functionality.

"""
from libraries.AudioManager import AudioManager
from libraries.RoombaBumper import RoombaBumper
from libraries.GPIOManager import GPIOManager

audio_manager = AudioManager()
gpio_manager = GPIOManager()
roomba_bumper = RoombaBumper(gpio_controller=gpio_manager, audio_controller=audio_manager)

# Primary try and except block
try:
    roomba_bumper.bumper_thread()

except KeyboardInterrupt:
    print("Done")

