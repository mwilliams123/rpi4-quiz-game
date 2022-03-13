from constants import GameState
from player import Player
from gpiozero import RGBLED
from pygame.time import Clock
import pygame

class PlayerManager():
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

    def green_light(self):
        self.stoplight.color = (0, 1, 0)
        self.timer = 5
        self.ticks = 0
        self.rung_in = None
        self.input = ''
        for p in self.players:
            p.eligible = True

    def poll(self, store):
        rungInYet = False
        et = self.clock.tick()
        self.ticks += 1
        for p in self.players:
           
            if p.active:
                rungInYet = True
                self.stoplight.color = (0,0,0)
                p.update_timer(et)
                if p.timer > 0:
                    return GameState.QUESTION, store
                else:
                    #question = store['clue']
                    return GameState.ANSWER, store
                
        if not rungInYet and self.ticks > 1:
           self.timer -= et
           if self.timer <= 0:
              return GameState.ANSWER, store   
             
        return GameState.QUESTION, store
    
    def ring_in(self, player):
        self.rung_in = player
        for p in self.players:
            p.eligible = False

    def update(self, correct, value):
        # update player score
        self.players[self.rung_in].answer_question(correct, value)
        # give control to player w/ correct answer
        if correct:
            self.control = self.rung_in
        print("Control: " + str(self.control))
            
    def update_control(self):
        # give control to player with lowest score at start of double jeopardy
        lowest = float('inf')
        for p in self.players:
            if p.score < lowest:
                lowest = p.score
                self.control = p.number
                
    def update_input(self, event):
        # update user input when key is pressed
        if event.key == pygame.K_BACKSPACE:
            self.input = self.input[:-1]
        else:
            self.input += event.unicode
            
        