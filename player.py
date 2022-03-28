"""
Manages player score, buzzer, and timers
"""
import threading
from gpiozero import Button, LED, Device
from gpiozero.pins.mock import MockFactory
from gpiozero.exc import BadPinFactory
# instance variables: score, eligible_to_ring, active, buzzer
#  eligible = possible to ring in after Alex asks the question
#  active = have rung in first and now can answer the question
#  timer = time left to answer questin

# constructor takes in led pin number and buzzer pin number

class Player:
    def __init__(self, led_pin, buzzer_pin, number, manager):
        self.active = False
        self.eligible = False
        self.score = 0
        self.timer = 5000
        self.player_answer = ""
        self.number = number
        self.manager = manager
        self.locked_out = False
        try:
            self.buzzer = Button(buzzer_pin)
            self.led = LED(led_pin)
        except BadPinFactory:
            Device.pin_factory = MockFactory()
            self.buzzer = Button(buzzer_pin)
            self.led = LED(led_pin)
        self.buzzer.when_pressed = self.buzz_in

    def buzz_in(self):
        """ Called when player buzzes in. """
        
        if self.eligible and not self.locked_out:
            self.active = True
            self.led.on()
            self.manager.ring_in(self.number)
            self.timer = 5000
        elif not self.locked_out:
            self.locked_out = True
            thread = threading.Timer(0.25, self.unlock)
            thread.start()

    def unlock(self):
        self.locked_out = False

    def answer_question (self, correct, value):
        """Determine if player gave correct answer and update score."""
        if correct:
            self.update_score(value)
        else:
            self.update_score(-value)

        self.active = False
        self.led.off()
        self.eligible = False
        self.timer = 5000

    def update_score (self, new_score):
        self.score += new_score

    def update_timer(self, elapsed_time):
        self.timer -= elapsed_time
