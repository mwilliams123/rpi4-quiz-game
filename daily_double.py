"""
Implement daily double
"""
from collections import namedtuple
import pygame
from constants import GameState, Colors
from util import TTS, SoundEffects, draw_text, Button, Fonts
from state import State

class DailyDouble(State):
    """Draws question"""
    def __init__(self):
        super().__init__()
        self.name = GameState.DAILY_DOUBLE
        self.show_answer = False
        self.clicked = False
        self.wager = None
        self.input = ''
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))
        self.timer = 6000

    def startup(self, store):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        store: a dict passed from state to state
        """
        SoundEffects.play(2)
        self.store = store
        self.clicked = False
        self.show_answer = False
        self.wager = None
        self.input = ''
        self.timer = 6000

    def handle_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True
        elif event.type == pygame.KEYDOWN:
            # update user input when key is pressed
            if event.key == pygame.K_BACKSPACE:
                self.input = self.input[:-1]
            else:
                self.input += event.unicode

    def update(self, player_manager, elapsed_time):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        if TTS.is_busy():
            return GameState.DAILY_DOUBLE

        if self.wager is None:
            if self.clicked and self.buttons.continue_button.was_clicked() and self.input.isdigit():
                self.wager = int(self.input)
                TTS.play_speech(self.store['clue']['answer'])
        else:
            if self.show_answer:
                # determine if button clicked
                if self.clicked:
                    player = player_manager.players[player_manager.control]
                    if self.buttons.correct_button.was_clicked():
                        player.answer_question(True,self.wager)
                        return GameState.BOARD
                    if self.buttons.wrong_button.was_clicked():
                        player.answer_question(False,self.wager)
                        return GameState.BOARD
            else:
                self.timer -= elapsed_time
                if self.timer <= 0:
                    SoundEffects.play(1)
                    self.show_answer = True
        self.clicked = False
        return GameState.DAILY_DOUBLE

    def draw(self, screen):
        """
        Draw everything to the screen.
        """
        # background color
        screen.fill(Colors.BLUE)
        width, height = screen.get_size()
        if self.wager is None:
            text = Fonts.NUMBER.render('DAILY DOUBLE', True, Colors.GOLD)
            rect = text.get_rect(center=(width/2, height/4))
            screen.blit(text,rect)
            self.buttons.continue_button.draw(screen, (width*1/2, height*3/4)) 
            # display wager
            text = Fonts.NUMBER.render('$' + self.input, True, Colors.WHITE)
            rect = text.get_rect(center=(width/2, height/2))
            screen.blit(text,rect)
        elif self.show_answer:
            text = self.store['clue']['question']
            draw_text(screen, text.upper(), Fonts.CLUE, (100, 100, width-100, height-100))
            # draw buttons
            self.buttons.correct_button.draw(screen, (width*1/4, height*3/4))
            self.buttons.wrong_button.draw(screen, (width*3/4, height*3/4))
        else:
            text = self.store['clue']['answer']
            draw_text(screen, text.upper(), Fonts.CLUE, (100, 100, width-100, height-100))
