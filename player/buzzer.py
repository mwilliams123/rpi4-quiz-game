"""
Interface for interacting with buzzer hardware.
"""
from gpiozero import Button, LED, Device
from gpiozero.pins.mock import MockFactory
from gpiozero.exc import BadPinFactory

class Buzzer:
    """Class representing a player's buzzer and led."""
    def __init__(self, led_pin, buzzer_pin, buzz_callback) -> None:
        try:
            self.buzzer = Button(buzzer_pin)
            self.led = LED(led_pin)
        except BadPinFactory:
            # Use mock hardware when not running on RPi
            Device.pin_factory = MockFactory()
            self.buzzer = Button(buzzer_pin)
            self.led = LED(led_pin)
        self.buzzer.when_pressed = buzz_callback

    def light_up(self):
        """Turn on player's led."""
        self.led.on()

    def light_off(self):
        """Turn off a player's light."""
        self.led.off()
