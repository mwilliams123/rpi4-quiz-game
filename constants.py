from enum import Enum

class GameState(Enum):
    QUIT = 0
    TITLE = 1
    MAIN = 2
    LOADING = 3

class Colors():
    BLUE = (6, 12, 233)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
