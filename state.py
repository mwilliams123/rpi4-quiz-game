"""
Template for implementing Game State classes.

Each game state must have an update() function for handling game logic
that returns the next game state, and a draw() function that draws the
current frame to the screen.

Game states may optionally implement their own startup() function to be
called once when a state is loaded, or a handle_event() function that
handles user input such as mouse clicks and keyboard presses.
"""
class State():
    """
    Abstract class for game states.

    Attributes:
        store (dict of str: Any): Dictionary of data that should be persistent and
            transfered from state to state
    """
    def __init__(self):
        self.store = {}

    def startup(self, store):
        """
        Executes once immediately after a state is transitioned into.

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        self.store = store

    def handle_event(self, event):
        """
        Controls logic for dealing with user input.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """

    def update(self, player_manager, elapsed_time):
        """Handles game logic.

        Called by the Game object once per frame. Should return the next game state.

        Args:
            player_manager (PlayerManager): reference to PlayerManager object that keeps track
                of players
            elapsed_time (int): Milliseconds that have passed since last time update() was called
        """
        raise NotImplementedError('update() not implemented for this State.')

    def draw(self, screen):
        """
        Draws the current frame to the screen.

        Args:
            screen (Surface): Pygame display where game will be drawn
        """
        raise NotImplementedError('draw() not implemented for this State.')
