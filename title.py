"""
Display Title screen.
"""
import pygame
from constants import GameState, Colors
from util import Button, Font
from state import State

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
        self.back = Button("Back")
        self.hosted_toggle = Button("OFF")
        self.show_options = False
        self.clicked = False
        self.initialize_store()

    def startup(self, store, player_manager):
        """
        Executes once immediately after a state is transitioned into.

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        self.store = {}
        self.initialize_store()

    def initialize_store(self):
        self.store['hosted'] = False
        self.store['n_players'] = 3

    def handle_event(self, event):
        """
        Sets flag when left mouse is clicked.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True

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
                self.show_options = True
            if self.back.was_clicked():
                self.show_options = False
            if self.hosted_toggle.was_clicked():
                self.store['hosted'] = not self.store['hosted']
                self.hosted_toggle.set_text('ON' if self.store['hosted'] else 'OFF')

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
        if self.show_options:
            self.back.draw(screen, (40, 20))
            text = Font.button.render("Hosted Mode", True, Colors.WHITE)
            text_rect = text.get_rect(center=(width/4, height/2))
            screen.blit(text, text_rect)
            self.hosted_toggle.draw(screen, (width*3/4, height/2))
        else:
            self.play_button.draw(screen, (width/2, height/3))
            self.hall_button.draw(screen, (width/2, height*3/4))
            self.options.draw(screen, (width/2, height*7/12))
