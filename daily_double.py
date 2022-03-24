"""
Implement daily double
"""
import pygame
from constants import GameState, Colors
from util import draw_text, play_speech, draw_button
from question import draw_question
from state import State

class DailyDouble(State):
    """Draws question"""
    def __init__(self):
        super().__init__()
        self.name = GameState.DAILY_DOUBLE
        self.font = pygame.font.Font('fonts/Caudex-Bold.ttf', 60)
        self.show_answer = False
        self.clicked = False
        self.wager = None
        self.play_sound  = True
        self.input = ''

    def startup(self, store):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        store: a dict passed from state to state
        """
        player_manager.sound_effects(2)
        self.store = store
        self.clicked = False
        self.show_answer = False
        self.wager = None

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
        if self.wager is None:
            if self.clicked and rect.collidepoint(pygame.mouse.get_pos()) and self.input.isdigit():
                self.wager = int(self.input)
                player_manager.timer = 6000
                self.play_sound = True
        else:
            # determine if button clicked
            if self.clicked:
                player = player_manager.players[player_manager.control]
                if correct_rect.collidepoint(pygame.mouse.get_pos()):
                    player.answer_question(True,player_manager.dd_wager)
                    return GameState.BOARD
                if wrong_rect.collidepoint(pygame.mouse.get_pos()):
                    player.answer_question(False,player_manager.dd_wager)
                    return GameState.BOARD
            player_manager.timer -= elapsed_time

        return GameState.DAILY_DOUBLE

    def draw(self, screen):
        """
        Draw everything to the screen.
        """
        # background color
        screen.fill(Colors.BLUE)
        width, height = screen.get_size()
        if self.wager is None:
            text = self.font.render('DAILY DOUBLE', True, Colors.GOLD)
            rect = text.get_rect(center=(width/2, height/4))
            screen.blit(text,rect)
            font = pygame.font.SysFont("arial", 40)
            text_rect = font.render('Continue', True, Colors.WHITE)
            rect = text_rect.get_rect(center=(width*1/2, height*3/4))
            screen.blit(text_rect,rect)
            # display wager
            text = font.render('$' + self.input, True, Colors.WHITE)
            rect = text.get_rect(center=(width/2, height/2))
            screen.blit(text,rect)
        else:
            text = self.store['clue']['question']
            width, height = screen.get_size()
            draw_text(screen, text.upper(), self.font, (100, 100, width-100, height-100))
            # draw buttons
            correct_rect = draw_button(screen, 'Correct', (width*1/4, height*3/4))
            wrong_rect = draw_button(screen, 'Incorrect', (width*3/4, height*3/4))
            draw_question(screen, self.store)
