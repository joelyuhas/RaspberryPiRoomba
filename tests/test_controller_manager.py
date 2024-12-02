"""
Joel Yuhas
April 2024

Controller Manager Test
----------------------

Very basic test that will instantiate the ControllerManager and grab the controller instance so it can be tested
against. The manual controller manager instantiation is available and commented out as well for verification if needed.

"""
import evdev
from evdev import InputDevice, categorize, ecodes
from libraries.ControllerManager import ControllerManager

# Default method if issue with the class
# ---------------------------------------------
# Find the Xbox controller device
# devices = [InputDevice(fn) for fn in evdev.list_devices()]
# for device in devices:
#    if "Xbox" in device.name:
#        xbox_controller = device
#        break
# else:
#    raise IOError("Xbox controller not found")

# Instantiate and initialize the controller using the class.
xbox_controller_object = ControllerManager()
xbox_controller = xbox_controller_object.get_controller_instance()

print("Using Xbox controller:", xbox_controller.name)

# Read input events from the Xbox controller
for event in xbox_controller.read_loop():
    if event.type == ecodes.EV_ABS:  # Analog input (joysticks and triggers)
        absevent = categorize(event)
        if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
            print("Left stick X axis:", absevent.event.value)
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
            print("Left stick Y axis:", absevent.event.value)
        # Add more conditions for other analog inputs as needed
    elif event.type == ecodes.EV_KEY:  # Digital input (buttons)
        if event.value == 1:  # Button pressed
            print("Button pressed:", event.code)
        elif event.value == 0:  # Button released
            print("Button released:", event.code)
        # Add more conditions for other buttons as needed
