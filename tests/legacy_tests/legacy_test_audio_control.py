"""
Legacy test used for basic instantiations and experimenting with calling audio files form the controller directly

"""
import RPi.GPIO as GPIO
import time


import evdev
from evdev import InputDevice, categorize, ecodes


import pygame.mixer
import time
import random


pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.mixer.init()  # turn all of pygame on.
AUDIO_DIRECTORY = "/home/pi/raspberrypi-items/roomba/audio/"

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


try:
    while True:

        time.sleep(0.1)
        # Read input events from the Xbox controller
        for event in xbox_controller.read_loop():
            if event.type == ecodes.EV_ABS:  # Analog input (joysticks and triggers)
                absevent = categorize(event)
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                    x_axis_value = absevent.event.value

                elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                    y_axis_value = absevent.event.value

                # Add more conditions for other analog inputs as needed
            elif event.type == ecodes.EV_KEY:  # Digital input (buttons)
                if event.value == 1:  # Button pressed
                    print("Button pressed:", event.code)
                    random_number = random.randint(1, 6)
                    sound = pygame.mixer.Sound(audio_file_list[random_number - 1])
                    sound.play()
                    time.sleep(sound.get_length())
                elif event.value == 0:  # Button released
                    print("Button released:", event.code)
                # Add more conditions for other buttons as needed


except KeyboardInterrupt:
    pass