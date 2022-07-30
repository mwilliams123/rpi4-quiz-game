"""
Define color and game state constants.
"""
from enum import Enum
from dataclasses import dataclass


class GameState(Enum):
    """Enums which represent the current game state.

    Attributes:
        TITLE: The title screen
        LOADING: The loading screen
        QUESTION: Screen for displaying, answering individual questions
        BOARD: The game board with clue values
        DAILY_DOUBLE: Special question screen
        INTRO: Category introduction screen
        FINAL: Final question screen
    """
    TITLE = 1
    LOADING = 2
    QUESTION = 3
    BOARD = 4
    DAILY_DOUBLE = 5
    INTRO = 6
    FINAL = 7
    HALL = 8
    TIE = 9
    STATS = 10

@dataclass
class Colors:
    """Constants that represent colors with RGB values."""
    BLUE = (10, 20, 140)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GOLD = (244, 152, 70)
    RED = (255,0,0)
