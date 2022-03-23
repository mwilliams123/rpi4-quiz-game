"""
Define color and game state constants
"""
from enum import Enum

class GameState(Enum):
    QUIT = 0
    TITLE = 1
    MAIN = 2
    LOADING = 3
    QUESTION = 4
    BOARD = 5
    ANSWER = 6
    INTRO = 7
    FINAL = 8
    DAILY_DOUBLE = 9

class Colors():
    BLUE = (10, 20, 140) #(6, 12, 233)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GOLD = (244, 152, 70)
    RED = (255,0,0)
