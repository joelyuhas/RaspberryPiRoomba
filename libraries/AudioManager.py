"""
Joel Yuhas
April 2024

Primary area for managing audio.

"""
import os
import glob

import pygame.mixer
import random
import time


class AudioManager:
    """
    Class that handles all the audio outputs through the speaker on the robot. Other classes can use this class to
    interface with the audio. Also used so that multiple classes do not need to perform their own instantiations and
    instead one class can handle the audio.

    """
    # The directory on the pi/roomba where the audio files are saved, hard coded.
    AUDIO_DIRECTORY = "/home/pi/git/raspberrypi-items/roomba/audio/"
    # Instead of looping as much as possible, have a sleeping period. Sleep constant can be toggled here.
    SLEEP_BETWEEN_LOOPS_SECONDS = 0.1

    def __init__(self):
        self.audio_files = []
        # Collect all .wav files in the given audio directory and save to file path. This way audio files can be added
        # and removed easily without needing to update the code each time.
        for file_path in glob.glob(os.path.join(self.AUDIO_DIRECTORY, '*.wav')):
            self.audio_files.append(file_path)
        self.pygame_instance = None
        self.initialize_audio()  # Initialize on startup

    def initialize_audio(self):
        """
        Method to initialize the pygame mixer for the audio and speaker connection.

        """
        pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
        pygame.mixer.init()  # Turn all of pygame on.

        self.pygame_instance = pygame.mixer

    def get_audio_instance(self):
        """
        Helper class to return the instance of the pygame audio mechanism when needed.

        """
        return self.pygame_instance

    def play_audio_file(self, audio_file: str):
        """
        Play a specific audio file. Pause for the length of time the file is being played.

        """
        sound = self.pygame_instance.mixer.Sound(audio_file)
        sound.play()
        time.sleep(sound.get_length())

    def play_random_sound(self):
        """
        Play a random sound on the speaker. Useful for when no certain sound is needed, just any sound.

        """
        # Get the number of audio files in the directory and select one randomly.
        random_number = random.randint(1, len(self.audio_files))
        sound = self.pygame_instance.mixer.Sound(self.audio_files[random_number - 1])
        sound.play()
        # Wait for the sound to fully play. Can also shorten to have only clips play.
        time.sleep(sound.get_length())

    def get_audio_list(self) -> list:
        """
        Basic helper function that returns the list of audio files. Useful for debugging.

        """
        return self.audio_files