"""
Display question
"""
import pygame
from constants import Colors, GameState
from util import draw_text, draw_button
from state import State

class Question(State):
    """Draws question"""
    def __init__(self):
        super().__init__()
        self.name = GameState.QUESTION
        self.font = pygame.font.Font('fonts/Caudex-Bold.ttf', 60)
        self.show_answer = False
        self.rang_in = False
        self.clicked = False

    def startup(self, store):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        store: a dict passed from state to state
        """
        self.store = store
        self.clicked = False
        self.show_answer = False
        self.rang_in = False

    def handle_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True

    def update(self, player_manager, elapsed_time):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        if player_manager.rung_in is None:
            if self.clicked and rect.collidepoint(pygame.mouse.get_pos()):
                return GameState.BOARD
        if self.show_answer:
            if correct_rect.collidepoint(pygame.mouse.get_pos()):
                player_manager.update(True,self.store['clue']['value'])
                return GameState.BOARD
            if wrong_rect.collidepoint(pygame.mouse.get_pos()):
                player_manager.update(False,self.store['clue']['value'])
                return GameState.BOARD
        return GameState.ANSWER

    def draw(self, screen):
        """
        Draw everything to the screen.
        """
        # background color
        screen.fill(Colors.BLUE)
        width, height = screen.get_size()
        if self.show_answer:
            # draw answer & continue buttons
            text = self.store['clue']['question']
            draw_text(screen, text.upper(), self.font, (100, 100, width-100, height-100))
            if self.rang_in:
                # draw buttons
                correct_rect = draw_button(screen, 'Correct', (width*1/4, height*3/4))
                wrong_rect = draw_button(screen, 'Incorrect', (width*3/4, height*3/4))
            else:
                continue_rect = draw_button(screen, 'Continue', (width*1/2, height*3/4))
        else:
            # draw question
            screen.fill(Colors.BLUE)
            text = self.store['clue']['answer']
            draw_text(screen, text.upper(), self.font, (100, 100, width-100, height-100))
