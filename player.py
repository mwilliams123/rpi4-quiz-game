"""
Manages player score, buzzer, and timers
"""
import threading
from gpiozero import Button, LED, Device
from gpiozero.pins.mock import MockFactory
from gpiozero.exc import BadPinFactory

class Player:
    """Representation of a player and associated hardware in the game.

    Attributes:
        active (boolean): True if player has rung in
        eligible (boolean): True when players are able to ring in after question is asked
        timer (int): Time in milliseconds left to answer question
        score (int): Player's current score value
        number (int): Player's id number
        manager (PlayerManager): reference to the player manager object
        locked_out (boolean): True when a player rung in too soon and is ineligible to ring in again
    """
    def __init__(self, led_pin, buzzer_pin, number, manager):
        """Instantiates Player Object

        Args:
            led_pin (int): GPIO pin number of player's light
            buzzer_pin (int): GPIO pin number of player's button
            number (int): Player's id number
            manager (PlayerManager): reference to the player manager object
        """
        self.active = False
        self.eligible = False
        self.score = 0
        self.timer = 5000
        self.number = number
        self.manager = manager
        self.locked_out = False
        try:
            self.buzzer = Button(buzzer_pin)
            self.led = LED(led_pin)
        except BadPinFactory:
            # Use mock hardware when not running on RPi
            Device.pin_factory = MockFactory()
            self.buzzer = Button(buzzer_pin)
            self.led = LED(led_pin)
        self.buzzer.when_pressed = self.buzz_in

    def buzz_in(self):
        """Called when player presses their button.

        Checks if player is allowed to ring in, locks them out for 0.25 seconds if they
        rung in too early."""

        if self.eligible and not self.locked_out:
            # Player rung in successfully
            self.active = True
            self.led.on()
            self.manager.ring_in(self.number)
            self.timer = 5000
        elif not self.locked_out:
            # Player rung in too early, lock them out
            self.locked_out = True
            thread = threading.Timer(0.25, self.unlock) # unlock after 0.25 seconds
            thread.start()

    def unlock(self):
        """Lets player ring in again. Called 0.25 seconds after lock out."""
        self.locked_out = False

    def answer_question (self, correct, value):
        """Adds clue's dollar amount to player's score if answer is correct,
        otherwise decrements their score. Resets player state.

        Args:
            correct (boolean): Whether the question was answered correctly
            value (int): Dollar amount of question
        """
        if correct:
            self.update_score(value)
        else:
            self.update_score(-value)

        self.active = False
        self.timer = 5000

    def update_score (self, amount):
        """Increments or decrements player score by amount.

        Args:
            amount (int): dollar value player has lost or won.
        """
        self.score += amount

    def update_timer(self, elapsed_time):
        """Decrements player timer by specified amount.

        Args:
            elapsed_time (int): time that has passed in milliseconds
        """
        self.timer -= elapsed_time
