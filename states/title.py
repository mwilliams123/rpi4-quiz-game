"""
Display Title screen.
"""
from util.constants import GameState, Colors
from util.util import Button, Font
from states.state import State

class TitleScreen(State):
    """Game State that shows a simple title screen and play button.

    Attributes:
        name (GameState): Enum that represents this game state
        play_button (Button): Button that can be clicked to start game
        clicked (boolean): whether the mouse has been clicked
        """
    def __init__(self):
        super().__init__()
        self.name = GameState.TITLE
        self.play_button = Button("Play", Font.get_font(Font.BIG))
        self.hall_button = Button("Hall of Fame")
        self.options = Button("Options")
        self.initialize_store()

    def startup(self, store, _player_manager):
        """
        Executes once immediately after a state is transitioned into.

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        self.store = store
        if 'n_players' not in store:
            self.initialize_store()

    def initialize_store(self):
        """Set default values for game options."""
        self.store['hosted'] = False
        self.store['n_players'] = 3

    def update(self, player_manager, elapsed_time):
        """
        Checks if start button has been clicked.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            GameState: Returns LOADING state when start button was clicked, otherwise continues
                to return TITLE state.
        """
        # determine if start button clicked
        if self.clicked:
            if self.play_button.was_clicked():
                return GameState.LOADING
            if self.hall_button.was_clicked():
                return GameState.HALL
            if self.options.was_clicked():
                return GameState.OPTIONS

        self.clicked = False # reset flag for next loop
        return GameState.TITLE

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
        self.play_button.draw(screen, (width/2, height/3))
        self.hall_button.draw(screen, (width/2, height*3/4))
        self.options.draw(screen, (width/2, height*7/12))
