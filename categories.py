"""
Read aloud categories and explanations.
"""
from constants import GameState, Colors
from state import State
from util import TTS, draw_text, Font

class IntroScreen(State):
    """
    Displays categories and introduces them using Text-to-Speech.

    Attributes:
        name (GameState): Enum that represents this game state
        categories (list of str): List of category names to be introduced
        index (int): Index of the current category being introduced
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.INTRO
        self.categories = []
        self.index = 0

    def startup(self, store, host):
        self.store = store
        self.index = 0
        # load categories for this round
        round_ = store['round']
        self.categories = list(store['data'][round_].keys())
        # Use Text-to-Speech
        TTS.play_speech("The categories are")

    def update(self, player_manager, elapsed_time, host):
        """Checks if last speech has finished, and if so, introduces next category.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            GameState: Returns BOARD game state when all categories have been introduced,
                otherwise continues to return INTRO game state
        """
        if not TTS.is_busy():
            if self.index >= len(self.categories):
                # return to game board when all categories have been introduced
                return GameState.BOARD
            # introduce next category
            text = self.categories[self.index]
            comments = self.store['data'][self.store['round']][text][0]['comments']
            if comments != '-':
                text += ' ' + comments # special category commentary
            TTS.play_speech(text)
            self.index += 1

        return GameState.INTRO

    def draw(self, screen):
        """Displays category name centered on blue background."""
        # background color
        screen.fill(Colors.BLUE)
        width, height = screen.get_size()
        if self.index >= 1:
            # draw text centered on screen with 100px buffer.
            draw_text(screen, self.categories[self.index - 1], Font.number,
                      (100, 100, width-100, height-100))
