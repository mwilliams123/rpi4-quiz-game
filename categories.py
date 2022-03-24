"""
Display category intro
"""
import time
import pygame
from constants import GameState, Colors
from state import State
from util import play_speech, draw_text

class IntroScreen(State):
    """
    Parent class for individual game states to inherit from.
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.INTRO
        self.font = pygame.font.Font('fonts/Anton-Regular.ttf', 60)

    def update(self, player_manager, elapsed_time):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        return GameState.BOARD

    def draw(self, screen):
        """Iterate through categories and explain each one"""
        play_speech("The categories are")
        time.sleep(1)
        width, height = screen.get_size()
        round_ = self.store['round']
        for cat in self.store['data'][round_]:
            screen.fill(Colors.BLUE)
            draw_text(screen, cat, self.font, (100, 100, width-100, height-100))
            pygame.display.flip()
            play_speech(cat)
            comments = self.store['data'][round_][cat][0]['comments']
            if comments != '-':
                play_speech(comments)
            time.sleep(0.25)
