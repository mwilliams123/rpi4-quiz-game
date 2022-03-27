"""
Display category intro
"""
from constants import GameState, Colors
from state import State
from util import TTS, draw_text, Fonts

class IntroScreen(State):
    """
    Parent class for individual game states to inherit from.
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.INTRO
        self.categories = []
        self.index = 0

    def startup(self, store):
        self.store = store
        TTS.play_speech("The categories are")
        round_ = store['round']
        print(store['data'][round_])
        self.categories = list(store['data'][round_].keys())

    def update(self, player_manager, elapsed_time):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        if not TTS.is_busy():
            if self.index >= len(self.categories):
                return GameState.BOARD
            text = self.categories[self.index]
            comments = self.store['data'][self.store['round']][text][0]['comments']
            if comments != '-':
                text += ' ' + comments
            TTS.play_speech(text)
            self.index += 1

        return GameState.INTRO

    def draw(self, screen):
        """Iterate through categories and explain each one"""
        width, height = screen.get_size()
        screen.fill(Colors.BLUE)
        if self.index >= 1:
            draw_text(screen, self.categories[self.index - 1], Fonts.NUMBER, (100, 100, width-100, height-100))
