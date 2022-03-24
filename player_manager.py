"""
Manage player timers and input
"""
from pygame.time import Clock
import pygame
from pygame import mixer
try:
    from gpiozero import RGBLED
except:
    print("wrong hardware")
from constants import GameState
from player import Player

mixer.init()
daily_double_sound = mixer.Sound("sounds/Jeopardy-daily2x.wav")
time_sound = mixer.Sound("sounds/Times-up.wav")
final_sound = mixer.Sound("sounds/Final-Music.wav")

class PlayerManager():
    """_summary_
    """
    def __init__(self):
        self.players = [Player(19, 6, 0, self), Player(16, 21, 1, self), Player(12, 17, 2, self)]
        self.timer = 5000
        self.clock = Clock()
        try:
            self.stoplight = RGBLED(red=18, blue=24, green=23)
        except:
            class Object(object):
                pass
            self.stoplight = Object()
        self.stoplight.color = (0,0,0)
        self.rung_in = None
        self.control = 0 # which player has control, starts w/ player 0
        self.ticks = 0
        self.dd_wager = None
        self.input = ''
        self.read_text = True
        self.dd_status = 0

    def green_light(self):
        """_summary_"""
        self.stoplight.color = (0, 1, 0)
        self.timer = 5000
        self.ticks = 0
        self.rung_in = None
        self.input = ''
        self.dd_status = 0
        self.read_text = False
        for player in self.players:
            player.eligible = True
            player.timer = 5000

    def poll(self, store):
        """_summary_

        Args:
            store (_type_): _description_

        Returns:
            _type_: _description_
        """
        rung_in_yet = False
        elapsed_time = self.clock.tick()
        self.ticks += 1
        for player in self.players:
            if player.active:
                rung_in_yet = True
                self.stoplight.color = (0,0,0)
                player.update_timer(elapsed_time)
                if player.timer > 0:
                    return GameState.QUESTION, store
                else:
                    self.sound_effects(1)
                    #question = store['clue']
                    return GameState.ANSWER, store

        if not rung_in_yet and self.ticks > 1:
            self.timer -= elapsed_time
            if self.timer <= 0:
                self.stoplight.color = (0,0,0)
                for player in self.players:
                    player.eligible = False
                time_sound.play()
                return GameState.ANSWER, store

        return GameState.QUESTION, store

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

    def update_input(self, event):
        # update user input when key is pressed
        if event.key == pygame.K_BACKSPACE:
            self.input = self.input[:-1]
        else:
            self.input += event.unicode

    def sound_effects(self, type_):
        if type_ == 1:
            time_sound.play()
        elif type_ == 2:
            daily_double_sound.play()
        else:
            final_sound.play()
