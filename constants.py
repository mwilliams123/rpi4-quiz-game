"""
Define color and game state constants
"""
from enum import Enum

class GameState(Enum):
    QUIT = 0
    TITLE = 1
    LOADING = 2
    QUESTION = 3
    BOARD = 4
    DAILY_DOUBLE = 5
    INTRO = 6
    FINAL = 7

class Colors():
    BLUE = (10, 20, 140) #(6, 12, 233)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GOLD = (244, 152, 70)
    RED = (255,0,0)
