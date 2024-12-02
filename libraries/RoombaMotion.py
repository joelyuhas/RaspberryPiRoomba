"""
Joel Yuhas
April 2024

Primary area for managing the motion and movement of the roomba.

"""
import RPi.GPIO as GPIO
from enum import Enum, auto

from GPIOManager import GPIOManager
from ControllerManager import ControllerManager
from evdev import InputDevice, categorize, ecodes


class Direction(Enum):
    """
    Basic enum class used to specify direction. Using an Enum offers more rigidity and is less prone to number errors
    over just using ints.

    """
    FORWARD = auto()
    BACKWARD = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()


class WheelSelector(Enum):
    """
    Basic Enum class used to specify what wheel to select. Using an Enum incase the wheels ever get expanded, will be
    easier to update.

    Note: Variables named LEFT/RIGHT/BOTH_WHEEL so not to get confused with Direction enum.

    """
    LEFT_WHEEL = auto()
    RIGHT_WHEEL = auto()
    BOTH_WHEEL = auto


class RoombaMotion:
    """
    Class that handles all motor speed calculations, motor controls. Intended to be an all encompassing class that given
    the properly instantiated controller and GPIO, this class will be the one place that will manage all the movement of
    the Roomba.

    """
    # Controller specific constants used for controlling the dead-zone
    DEAD_ZONE_MIDDLE = 32767
    DEAD_ZONE_AMOUNT = 7500
    DEAD_ZONE_LOWER = DEAD_ZONE_MIDDLE - DEAD_ZONE_AMOUNT
    DEAD_ZONE_UPPER = DEAD_ZONE_MIDDLE + DEAD_ZONE_AMOUNT
    DEAD_ZONE_RANGE = DEAD_ZONE_LOWER
    DEAD_ZONE_MAX = 65535

    def __init__(self, gpio_controller: GPIOManager, xbox_controller: ControllerManager):
        self.gpio_controller = gpio_controller
        # Get just the instants of the xbox controller that is managed by the ControllerManager
        self.xbox_controller = xbox_controller.get_controller_instance()

    def wheel_control(self, wheel: WheelSelector, direction: Direction):
        """
        Takes care of the controlling the inputs for the either left or right wheel. Since this is controlling the
        H-bridge, it requires 2 GPIO for each wheel. When the H bridge pins are toggled specific ways, that controls
        if the wheel goes forwards, backwards, or stops.

        Designed to handle one wheel at a time so each can be controlled individually if needed.

        :param wheel: WheelSelector: Either LEFT_WHEEL or RIGHT_WHEEL
        :param direction: Direction: Either FORWARD, BACK, or STOP constant in int format.

        """
        # Select the Wheel
        if wheel == WheelSelector.RIGHT_WHEEL:
            pin_1 = self.gpio_controller.INPUT_PIN_1
            pin_2 = self.gpio_controller.INPUT_PIN_2
        else:
            pin_2 = self.gpio_controller.INPUT_PIN_3
            pin_1 = self.gpio_controller.INPUT_PIN_4

        # Select the direction for this specific wheel
        if direction == Direction.FORWARD:
            GPIO.output(pin_1, GPIO.HIGH)
            GPIO.output(pin_2, GPIO.LOW)
        elif direction == Direction.BACKWARD:
            GPIO.output(pin_1, GPIO.LOW)
            GPIO.output(pin_2, GPIO.HIGH)
        elif direction == Direction.STOP:
            GPIO.output(pin_1, GPIO.LOW)
            GPIO.output(pin_2, GPIO.LOW)

    def set_motor_direction(self, direction: Direction):
        """
        Control how the wheel motors move relative to each other depending on which motion direction is selected.

        :param direction: Direction: Either FORWARD, BACK, STOP, LEFT, or RIGHT.

        """
        if direction == Direction.BACKWARD or direction == Direction.FORWARD or direction == Direction.STOP:
            self.wheel_control(WheelSelector.RIGHT_WHEEL, direction)
            self.wheel_control(WheelSelector.LEFT_WHEEL, direction)
        elif direction == Direction.RIGHT:
            self.wheel_control(WheelSelector.RIGHT_WHEEL, Direction.BACKWARD)
            self.wheel_control(WheelSelector.LEFT_WHEEL, Direction.FORWARD)
        elif direction == Direction.LEFT:
            self.wheel_control(WheelSelector.RIGHT_WHEEL, Direction.FORWARD)
            self.wheel_control(WheelSelector.LEFT_WHEEL, Direction.BACKWARD)
        else:
            self.wheel_control(WheelSelector.LEFT_WHEEL, Direction.STOP)
            self.wheel_control(WheelSelector.RIGHT_WHEEL, Direction.STOP)

# Function to set motor speed
    def set_motor_speed(self, wheel: WheelSelector = WheelSelector.BOTH_WHEEL, speed: int = 0):
        """
        Set the speed of either the left, right or both motors.

        :param wheel: WheelSelector:  either LEFT, RIGHt, or BOTH
        :param speed: int: The speed for the motors, between 0-100

        """
        if wheel == WheelSelector.LEFT_WHEEL:
            self.gpio_controller.pwm1.ChangeDutyCycle(speed)
        elif wheel == WheelSelector.RIGHT_WHEEL:
            self.gpio_controller.pwm2.ChangeDutyCycle(speed)
        elif wheel == WheelSelector.BOTH_WHEEL:
            self.gpio_controller.pwm1.ChangeDutyCycle(speed)
            self.gpio_controller.pwm2.ChangeDutyCycle(speed)
        else:
            pass

    def set_wheel_balance(self, x_value: int, desired_speed: int):
        """
        Depending on where the left stick on the controller is, set the "balance" between the wheels. This is the
        relative speed of the wheels between each-other, so slight turns can be done when the analog stick is only
        slightly pointed off center, and more aggressive turns can be done the further the analog stick is from the
        center.

        :param x_value: int: The raw value of the x-axis position of the left analog stick.
        :param desired_speed: int: The desired total speed of the motor from 0-100, 0 being no speed, 100 being full
                                    speed.

        """
        # Check how far the left stick is from the middle of the dead zone (neutral position) and get and turn into
        # percentage
        distance_from_deadzone = x_value - self.DEAD_ZONE_MIDDLE
        percentage = (distance_from_deadzone / self.DEAD_ZONE_MIDDLE)

        # Invert the percentage, the closer to the center, the closer to equal the wheels should be  balanced, the
        # further from the center, the greater the wheel power difference will be.
        invert_percentage = 1 - abs(percentage)

        # If the original percentage is negative, command to turning left.
        if percentage < 0:
            self.set_motor_speed(WheelSelector.LEFT_WHEEL, desired_speed)
            self.set_motor_speed(WheelSelector.RIGHT_WHEEL, int(desired_speed * invert_percentage))

        # Else, command is to turn right:
        else:
            self.set_motor_speed(WheelSelector.RIGHT_WHEEL, desired_speed)
            self.set_motor_speed(WheelSelector.LEFT_WHEEL, int(desired_speed * invert_percentage))

    def calculate_turning_speed(self, x_value: int) -> int:
        """
        Calculate how fast the robot should turn from 0-100 based on the x_value from the analog stick. The closer the
        analog stick is to the edge, the faster the speed should go. This way, if the user only moves the analog stick
        a small amount, the robot will go slowly instead of full speed.

        :param x_value: int: The raw value of the x-axis position of the left analog stick.
        :return: int: The speed the robot should turn based on the input from the x value.

        """
        absolute_value = x_value - self.DEAD_ZONE_MIDDLE

        return_value = int(abs((absolute_value / self.DEAD_ZONE_MIDDLE) * 100))

        # Cap at 100
        if return_value >= 100:
            return 100

        return return_value

    def calculate_directional_speed(self, y_value: int) -> int:
        """
        Calculate how fast the robot should move either forward or backwards based on the position of the y-axis of the
        left analog stick. The closer the analog stick is to the edge, the faster the robot will go. This way the user
        can control the speed with the analog stick.

        :param y_value: int: The raw value of the y-axis position of the left analog stick.
        :return: int: The value from 0-100 of how fast the robot should go for the PWM
        """
        absolute_value = y_value - self.DEAD_ZONE_MIDDLE

        # If negative, send the robot backwards
        if absolute_value < 0:
            self.set_motor_direction(Direction.FORWARD)

        # Otherwise, send the robot forwards
        else:
            self.set_motor_direction(Direction.BACKWARD)

        return int(abs((absolute_value / self.DEAD_ZONE_MIDDLE) * 100))

    def motion_thread(self):
        """
        The primary thread for reading from the controller and turning the controller inputs into motor outputs.

        """
        x_axis_value = 0
        y_axis_value = 0

        # Main motion loop. Every time the controller is updated, an event is produced.
        for event in self.xbox_controller.read_loop():
            if event.type == ecodes.EV_ABS:  # joystick input
                absevent = categorize(event)
                # Getting X axis value
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                    x_axis_value = absevent.event.value

                # Getting Y axis value
                elif ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                    y_axis_value = absevent.event.value

                # if in analog stick dead-zone, set movement to 0
                if self.DEAD_ZONE_LOWER < x_axis_value < self.DEAD_ZONE_UPPER and self.DEAD_ZONE_LOWER < y_axis_value \
                        < self.DEAD_ZONE_UPPER:
                    self.set_motor_direction(Direction.STOP)

                # if Y in dead zone, but X to the right, perform hard right turn
                elif 65536 > x_axis_value > self.DEAD_ZONE_UPPER > y_axis_value > self.DEAD_ZONE_LOWER:
                    p = self.calculate_turning_speed(x_axis_value)
                    self.set_motor_speed(WheelSelector.BOTH_WHEEL, p)
                    self.set_motor_direction(Direction.RIGHT)

                # if Y in dead zone, but X to the left, perform hard left turn
                elif 0 <= x_axis_value < self.DEAD_ZONE_LOWER < y_axis_value < self.DEAD_ZONE_UPPER:
                    turning_speed = self.calculate_turning_speed(x_axis_value)
                    self.set_motor_speed(WheelSelector.BOTH_WHEEL, turning_speed)
                    self.set_motor_direction(Direction.LEFT)

                # If none of the above conditions, calculate and perform speed update for going forward or backwards
                else:
                    percentage = self.calculate_directional_speed(y_axis_value)
                    self.set_wheel_balance(x_axis_value, percentage)

            # Future update area to add more conditions for other analog inputs as needed.
            elif event.type == ecodes.EV_KEY:  # Digital input (buttons)
                if event.value == 1:  # Button pressed
                    print("Button pressed:", event.code)
                elif event.value == 0:  # Button released
                    print("Button released:", event.code)
                # Add more conditions for other buttons as needed


