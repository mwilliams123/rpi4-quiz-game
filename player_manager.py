from constants import GameState
from player import Player
from gpiozero import RGBLED
from pygame import clock
class PlayerManager():
    def __init__(self):
        self.players = [Player(19, 6), Player(16, 21), Player(12, 17)]
        self.timer = 5

    def green_light(self):
        stoplight = RGBLED(red=18, blue=24, green=23)
        stoplight.color = (0, 1, 0)
        
        for p in self.players:
            p.eligible - True

    def poll(self, store):
        et = clock.tick()
        for p in self.players:
            if p.active:
                p.update_timer(et)
                if p.timer > 0:
                    store['timer'] = p.timer
                    return GameState.QUESTION, store
                else:
                    question = store['clue']
                    p.answer_question(question['question'], question['value'])
                    return GameState.BOARD, store
        return GameState.QUESTION, store
