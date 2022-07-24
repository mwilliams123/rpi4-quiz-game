"""
Manages player score, buzzer, and timers
"""
import threading
from gpiozero import Button, LED, Device
from gpiozero.pins.mock import MockFactory
from gpiozero.exc import BadPinFactory

from player_stats import PlayerStats

class Player:
    """Representation of a player and associated hardware in the game.

    Attributes:
        eligible (boolean): True when players are able to ring in after question is asked
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
        self.eligible = False
        self.score = 0
        self.number = number
        self.manager = manager
        self.locked_out = False
        self.stats = PlayerStats()
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
            self.manager.ring_in(self.number)
            self.stats.record_buzzer()
            self.led.on()
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
        otherwise decrements their score.

        Args:
            correct (boolean): Whether the question was answered correctly
            value (int): Dollar amount of question
        """
        if correct:
            self.score += value
        else:
            self.score -= value
