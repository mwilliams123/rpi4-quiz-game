"""
Display Options screen.
"""
from util.constants import GameState, Colors
from util.util import Button, Font
from states.state import State

class OptionsScreen(State):
    """Game State that shows a simple Options screen and play button.

    Attributes:
        name (GameState): Enum that represents this game state
        play_button (Button): Button that can be clicked to start game
        clicked (boolean): whether the mouse has been clicked
        """
    def __init__(self):
        super().__init__()
        self.name = GameState.OPTIONS
        self.back = Button("Back")
        self.hosted_toggle = Button("OFF")
        self.num_players_toggle = Button("3")
        self.store = {}
        self.initialize_store()

    def startup(self, store, _player_manager):
        """
        Executes once immediately after a state is transitioned into.

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        self.store = {}
        self.initialize_store()

    def initialize_store(self):
        """Assign default values for game options."""
        self.store['hosted'] = False
        self.store['n_players'] = 3

    def update(self, player_manager, elapsed_time):
        """
        Toggle options when they are clicked.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            GameState: Returns TITLE state when back button was clicked, otherwise continues
                to return OPTIONS state.
        """
        # determine if start button clicked
        if self.clicked:
            if self.back.was_clicked():
                return GameState.TITLE
            if self.hosted_toggle.was_clicked():
                self.store['hosted'] = not self.store['hosted']
                self.hosted_toggle.set_text('ON' if self.store['hosted'] else 'OFF')
            if self.num_players_toggle.was_clicked():
                self.store['n_players'] = self.store['n_players'] + 1
                if self.store['n_players'] > 5:
                    self.store['n_players'] = 2
                self.num_players_toggle.set_text(str(self.store['n_players']))

        self.clicked = False # reset flag for next loop
        return GameState.OPTIONS

    def draw(self, screen):
        """
        Draws play button on simple black background.

        Args:
            screen (Surface): Pygame display where game will be drawn
        """
        # background color
        screen.fill(Colors.BLACK)

        # draw start button in center of screen
        width, height = screen.get_size()
        self.back.draw(screen, (40, 20))
        text = Font.button.render("Hosted Mode", True, Colors.WHITE)
        text_rect = text.get_rect(center=(width/4, height/2))
        screen.blit(text, text_rect)
        self.hosted_toggle.draw(screen, (width*3/4, height/2))

        text = Font.button.render("Num Players", True, Colors.WHITE)
        text_rect = text.get_rect(center=(width/4, height/2 + 100))
        screen.blit(text, text_rect)
        self.num_players_toggle.draw(screen, (width*3/4, height/2 + 100))
