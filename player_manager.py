"""
Manage player timers and input
"""
import pygame
import gpiozero
from util import SoundEffects
from player import Player

class PlayerManager():
    """_summary_
    """
    def __init__(self):
        self.players = [Player(19, 6, 0, self), Player(16, 21, 1, self), Player(12, 17, 2, self)]
        self.timer = 5000
        self.clock = pygame.time.Clock()
        try:
            self.stoplight = gpiozero.RGBLED(red=18, blue=24, green=23)
        except gpiozero.exc.PinPWMUnsupported:
            class MockRGB():
                pass
            self.stoplight = MockRGB()
        self.stoplight.color = (0,0,0)
        self.rung_in = None
        self.control = 0 # which player has control, starts w/ player 0
        self.timer_started = False

    def green_light(self):
        """_summary_"""
        self.stoplight.color = (0, 1, 0)
        self.rung_in = None
        for player in self.players:
            player.eligible = True
            player.timer = 5000

    def poll(self, elapsed_time):
        """_summary_

        Args:
            store (_type_): _description_

        Returns:
            _type_: _description_
        """
        if self.rung_in is not None:
            self.stoplight.color = (0,0,0)
            return True
        self.timer -= elapsed_time
        if self.timer <= 0:
            self.stoplight.color = (0,0,0)
            for player in self.players:
                player.eligible = False
            SoundEffects.play(1)
            return True

        return False

    def ring_in(self, player):
        self.rung_in = player
        for player in self.players:
            player.eligible = False
        

    def update(self, correct, value):
        # update player score
        self.players[self.rung_in].answer_question(correct, value)
        # give control to player w/ correct answer
        if correct:
            self.control = self.rung_in

    def update_control(self):
        # give control to player with lowest score at start of double jeopardy
        lowest = float('inf')
        for player in self.players:
            if player.score < lowest:
                lowest = player.score
                self.control = player.number
