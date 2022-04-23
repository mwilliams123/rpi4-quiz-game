"""
Display Title screen.
"""
import pygame
from constants import GameState, Colors
from util import Button
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
        self.play_button = Button("Play")
        self.clicked = False

    def handle_event(self, event):
        """
        Sets flag when left mouse is clicked.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True

    def update(self, player_manager, elapsed_time, host):
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
        if self.clicked and self.play_button.was_clicked():
            return GameState.LOADING

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
        self.play_button.draw(screen, (width/2, height/2))
