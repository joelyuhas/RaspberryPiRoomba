"""
Joel Yuhas
April 2024

Primary area for managing the GPIO.

"""
import RPi.GPIO as GPIO


class GPIOManager:
    """
    Class that handles the GPIO instantiation. The GPIO pins are very specific to how the raspberry pi is currently
    configured, so the pin values are put as class variables that can be easily modified by the user. Decided to use
    class variables instead of constants so its tied directly to the class.

    == CURRENT LAYOUT NOTES ==
    --------------------------
    - pin-outs for the roomba bumpers
        - left bumper
            ORANGE:         VCC (3.3vv)
            BROWN / YELLOW: (connects to yellow on the other right bumper, so yellow) GND
            GREY:           VCC
            BLACK:          Output ((3.3vv high bumper not blocked, low when blocked)

        - right bumper
            BROWN:  (from left bumper) VCC
            YELLOW: GND
            PURPLE: VCC (3.3v)
            BLACK:  Output

    """
    # the GPIO bumper pins being used to read the bumper outputs
    BUMPER_PIN_1 = 16
    BUMPER_PIN_2 = 26

    # GPIO for controlling the motors
    ENABLE_PIN_1 = 18
    ENABLE_PIN_2 = 12
    INPUT_PIN_1 = 23
    INPUT_PIN_2 = 24
    INPUT_PIN_3 = 17
    INPUT_PIN_4 = 27

    def __init__(self):
        self.pwm1 = None
        self.pwm2 = None
        self.initialize_gpio()  # Initialize on startup

    def initialize_gpio(self):
        """
        Initialize the GPIO pins

        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ENABLE_PIN_1, GPIO.OUT)
        GPIO.setup(self.ENABLE_PIN_2, GPIO.OUT)
        GPIO.setup(self.INPUT_PIN_1, GPIO.OUT)
        GPIO.setup(self.INPUT_PIN_2, GPIO.OUT)
        GPIO.setup(self.INPUT_PIN_3, GPIO.OUT)
        GPIO.setup(self.INPUT_PIN_4, GPIO.OUT)

        # Set PWM for speed control
        self.pwm1 = GPIO.PWM(self.ENABLE_PIN_1, 100)
        self.pwm2 = GPIO.PWM(self.ENABLE_PIN_2, 100)
        self.pwm1.start(0)  # Start PWM with duty cycle 0
        self.pwm2.start(0)  # Start PWM with duty cycle 0

        # Set up the GPIO pin for input
        GPIO.setup(self.BUMPER_PIN_1, GPIO.IN)
        GPIO.setup(self.BUMPER_PIN_2, GPIO.IN)

    def cleanup(self):
        """
        Perform the standard cleanup for the gpio on the Pi

        """
        self.pwm1.stop()
        self.pwm2.stop()
        GPIO.cleanup()
