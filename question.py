"""
Display question
"""
from collections import namedtuple
import pygame
from constants import Colors, GameState
from util import SoundEffects, draw_text, Button, TTS, Fonts
from state import State

class Question(State):
    """Draws question"""
    def __init__(self):
        super().__init__()
        self.name = GameState.QUESTION
        self.show_answer = False
        self.rang_in = False
        self.clicked = False
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))
        self.timer = 5000

    def startup(self, store):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        store: a dict passed from state to state
        """
        TTS.play_speech(store['clue']['answer'])
        self.store = store
        self.clicked = False
        self.show_answer = False
        self.rang_in = False
        self.timer = 5000

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
        if TTS.is_busy():
            return GameState.QUESTION
        if self.timer == 5000:
            player_manager.green_light()

        if self.show_answer:
            if player_manager.rung_in is None:
                if self.clicked and self.buttons.continue_button.was_clicked():
                    return GameState.BOARD
            elif self.clicked:
                if self.buttons.correct_button.was_clicked():
                    player_manager.update(True,self.store['clue']['value'])
                    return GameState.BOARD
                if self.buttons.wrong_button.was_clicked():
                    player_manager.update(False,self.store['clue']['value'])
                    return GameState.BOARD
        else:
            self.timer -= elapsed_time
            if player_manager.rung_in is None:
                if self.timer <= 0:
                    self.show_answer = True
                    SoundEffects.play(1)
            else:
                self.rang_in = True
                # wait for player response
                if player_manager.poll(elapsed_time):
                    self.show_answer = True

        return GameState.QUESTION

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
            draw_text(screen, text.upper(), Fonts.CLUE, (100, 100, width-100, height-100))
            if self.rang_in:
                # draw buttons
                self.buttons.correct_button.draw(screen, (width*1/4, height*3/4))
                self.buttons.wrong_button.draw(screen, (width*3/4, height*3/4))
            else:
                self.buttons.continue_button.draw(screen, (width*1/2, height*3/4))
        else:
            # draw question
            screen.fill(Colors.BLUE)
            text = self.store['clue']['answer']
            draw_text(screen, text.upper(), Fonts.CLUE, (100, 100, width-100, height-100))
