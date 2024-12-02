"""
Joel Yuhas
April 2024

AudioManager Test
----------------------------

Very basic audio control test that instantiates the AudioManager, plays a random sound, and then will continually play
all the sounds in the audio list until a keyboard interrupt cancels.

Useful for manual debugging and testing audio files and the AudioManager class.

"""
from libraries.AudioManager import AudioManager

audio_manager = AudioManager()
print("Attempting to play a random sound")
audio_manager.play_random_sound()

# Get all the audio files currently saved
audio_files = audio_manager.get_audio_list()

# Attempt to loop through and play all the audio files until the user performs a Keyboard Interrupt
try:
    while True:
        print("Attempting to play files")
        for audio_file in audio_files:
            print("Playing: " + audio_file)
            audio_manager.play_audio_file(audio_file)

except KeyboardInterrupt:
    print("Done")