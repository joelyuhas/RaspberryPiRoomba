"""
Joel Yuhas
April 2024

Camera Control Test
---------------------

Currently, in the very early prototype stages, being used to manually test and verify the PiCamera functionality.

"""
from picamera import PiCamera


camera = PiCamera()

camera.capture("/media/pi/C2F3-961E/test_01.jpg")
