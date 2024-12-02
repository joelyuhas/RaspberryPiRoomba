"""
Joel Yuhas
April 2024

RoombaMotion Test
----------------------

Full motor and motion control test. Only instantiates the RoombaMotion and dependant classes. Used for manual testing,
RoombaMotion testing, and to ensure the core movement mechanics work.

"""
from libraries.RoombaMotion import RoombaMotion
from libraries.ControllerManager import ControllerManager
from libraries.GPIOManager import GPIOManager

# Initialize the core classes needed
controller_manager = ControllerManager()
gpio_manager = GPIOManager()
roomba_motion = RoombaMotion(xbox_controller=controller_manager,
                             gpio_controller=gpio_manager)

# Primary try and except block, properly cleans up on keyboard interrupt.
try:
    roomba_motion.motion_thread()

except KeyboardInterrupt:
    gpio_manager.cleanup()


