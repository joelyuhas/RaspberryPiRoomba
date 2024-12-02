"""
Older test used for attempting to get a certain audio codex working on the raspberry pi. Ultimately was unsuccessful but
leaving in legacy tests in case it ever gets picked up again.

"""
import pygame
import RPi.GPIO as GPIO
import time

AUDIO_DIRECTORY = "/home/pi/raspberrypi-items/roomba/audio/"

audio_file_list = [AUDIO_DIRECTORY + "1.wav",
                   AUDIO_DIRECTORY + "2.wav",
                   AUDIO_DIRECTORY + "3.wav",
                   AUDIO_DIRECTORY + "4.wav",
                   AUDIO_DIRECTORY + "5.wav",
                   AUDIO_DIRECTORY + "6.wav"]


# Define GPIO pin numbers for audio output
LRC_PIN = 19
BCLK_PIN = 18
DIN_PIN = 21

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([LRC_PIN, BCLK_PIN, DIN_PIN], GPIO.OUT)

# Initialize pygame mixer
pygame.mixer.init()

# Load and play audio file
pygame.mixer.music.load(audio_file_list[0])  # Replace 'example.mp3' with your audio file path
pygame.mixer.music.play()

# Wait while the audio is playing
while pygame.mixer.music.get_busy():
    time.sleep(1)

# Clean up GPIO
GPIO.cleanup()