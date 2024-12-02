# RaspberryPiRoomba
A modified Roomba controlled by a Raspberry Pi and supporting hardware mounted inside. The Pi was able to read from the bumper sensors, play audio, connect via bluetooth to an xbox controller, use the controller input to activate the motors, and more!

Several breadboards, voltage regulators, batteries, and other items were used so the roomba could operate as an independent system (no external physical connections needed). Several modifications were also done to the roomba and its motors/sensors so the Pi could interface with them.  

This project was a fantastic learning experience using software development, electrical engineering principals, and robotics! 

Originally created April 2024. Work continuing today.

## Objective
The objective of this project was to take an old, Roomba 610 model with a broken motherboad, find a way to put a Raspberry Pi inside it, and use the Pi to control the Roomba. 

Ideally, the Roomba would be independent, meaning it could rely on an internal battery for power and didnt need external physical connections, and would only rely on an xbox controller for input.

## Setup
The following are some of the items that were used for this project:
- Roomba 610 model (broken motherboard, working motors and bumper sensors)
- Replacement Roomba battery
- Raspberry Pi
- LM2596 DC to DC Voltage Regulator (x2) 
- L298N Motor Driver
- Mini battery powered speaker

## High Level Overview
This project had two main portions to it, the physical hardware setup and the software setup.

### Physical Hardware Setup
The following is a brief rundown of how the hardware was setup for this project.
1. The roomba was torn down, deep cleaned, and put back together, removing the broken motherboad, dust bin motor, and primary brush rollers on the underside.
   - Removing the dust bin motor and brush motors left plenty of room for the Pi and other devices to be mounted internally.
2. The old battery was replaced with a new battery.
3. The Raspberry Pi, motor driver, and voltage regulators, were mounted in the cavity where the main roller brushes were previously located.
4. The voltage regulator was used to step the battery voltage down from 14.8V to 5V so the Raspberry Pi, motor driver, and a few sensors could use it.
5. The bumper IR sensors were connected to a bread board that was placed where the motherboard used to be in the roomba.
   - To ensure the sensors worked, voltage dividing and pull down resistors were needed to interface with the IR sensors.
6. Another voltae regulator was used to step down the Battery 14.8V to 9V for the wheel motors.
7. The motor driver was connected to 9V voltage regulator and the wheel motors on the roomba.
   - The ports to the wheel motors had to be modified so that clean connections could be made to just the positive and negative terminals.   
8. The bread board for the bumper sensors, as well as the motor driver and command signals were all linked to the Pi's GPIO pins.
9. A small, battery powered speaker was mounted in the Roomba dust bin cavity and connected to the Pi via an aux cable.


### Software Setup
The code that ran on the Pi is present in this GitHub repo. A class based, object oriented design was chosen to make the code easy to read, compartmentalized, easy to maintain, and scaleable. Future plans to expand off this project exist, so a strong foundation was desired so it could be built off of. Several wrapper and handler classes were used.

A high level overview of the code is shown in the following:

#### Libraries Directory
- Contains all the primary classes that are used.
- The three "Manager" classes are designed to be responsible for one specific functionality on the roomba, to keep it organized and allow other code to easily access that functionality. These include:
   - AudioManager: Handles organizing the audio files, setting up the audio drivers, and playing audio.
   - ControllerManager: Responsible for instantiating the xbox controller and reading its inputs.
   - GPIOManager: Responsible for initializing the GPIO on the Pi and helping send/receive signals when needed.
- The two "Roomba" classes are designed to run their own respective thread, that monitors and performs some logic on the roomba.
  - RoombaMotion: Takes the controller input and based on the left analog stick's values, controls the two wheel motors to drive the roomba in a specific direction.
  - RoombaBumper: Reads the bumper sensor input and if a hit is detected, play a random sound.

#### Tests Directory
- Contains the tests that were used when updating the roomba software and hardware.
- Some tests instantiate the classes so they can be tested for functionality, others initiate all modules directly so they can be used as sanity checks if the classes stop working.

#### Audio Directory
- Contains the audio files, need to be in .wav format (original .mp3 format files were left as backups).
- The AudioManager class automatically scans this directory and compiles a dynamic list of all valid files on startup.

#### run_roomba.py
- The primary file that starts all the desired programs.
- Set to auto run on the Pi startup. 

## Future Updates
Several future updates are planned, as well as a few improvements that will be done to make the code even more scaleable and compartmentalized.

A more detailed writeup in PDF format coming soon!
