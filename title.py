"""
Title screen
"""
import pygame
from constants import GameState, Colors
from state import State

class TitleScreen(State):
    """Draws title screen and play button."""
    def __init__(self):
        super().__init__()
        self.name = GameState.TITLE
        self.font = pygame.font.SysFont("arial", 60)
        self.text = self.font.render("Play", True, Colors.WHITE)
        width, height = pygame.display.get_surface().get_size()
        self.text_rect = self.text.get_rect(center=(width/2, height/2))
        self.start_clicked = False

    def handle_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            print("clicked")
            self.start_clicked = True

    def update(self, player_manager, elapsed_time):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        # determine if start button clicked
        if self.start_clicked and self.text_rect.collidepoint(pygame.mouse.get_pos()):
            return GameState.LOADING

        return GameState.TITLE

    def draw(self, screen):
        """
        Draw everything to the screen.
        """
        # background color
        screen.fill(Colors.BLACK)

        # draw start button
        screen.blit(self.text,self.text_rect)
