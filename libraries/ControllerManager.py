"""
Joel Yuhas
April 2024

Primary area for managing the controller instantiation.

"""
import evdev
import time

from evdev import InputDevice, categorize, ecodes


class ControllerManager:
    """
    Class used to instantiate the xbox controller interface and  pass it to other classes. Having this in its own class
    allows other classes to easily be able to get its values, vs having individual classes do their own instantiations .
    This ensures that multiple classes can use the controller vs just whichever one instantiated it first.

    """
    def __init__(self):
        self.xbox_controller = None
        self.initialize_xbox_controller()  # Initialize on startup

    def initialize_xbox_controller(self):
        """
        Attempt to establish a connection to the controller. Try max_attempts.

        """
        max_attempts = 15  # Maximum number of retry attempts
        current_attempts = 0  # Initialize attempts counter

        while current_attempts < max_attempts:
            try:
                self.find_xbox_controller()
                break
            except IOError:
                current_attempts += 1
                print(f"Controller not connected, attempt: {current_attempts}")
                time.sleep(2)

    def find_xbox_controller(self):
        """
        Attempt to find and initialize the xbox controller if it exists.

        """
        # Find the Xbox controller device
        devices = [InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            if "Xbox" in device.name:
                self.xbox_controller = device
                break
        else:
            raise IOError("Xbox controller not found")

        print("Using Xbox controller:", self.xbox_controller.name)

    def get_controller_instance(self) -> InputDevice:
        """
        Return the xbox controller instance. This could also be done by just calling the self.xbox_controller, but
        having a method makes it more direct.

        :return: the Xbox controller instance

        """
        return self.xbox_controller

