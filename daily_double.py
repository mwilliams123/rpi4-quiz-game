"""
Implement Daily Double
"""
from collections import namedtuple
import pygame
from constants import GameState, Colors
from util import TTS, SoundEffects, draw_text, Button, Font
from state import State

class DailyDouble(State):
    """Handles the implementation of Daily Double questions.

    Allows a player to enter a wager, then displays a question on screen. After
    a timer runs out, shows the answer and prompts the user to click if the reponse
    was correct or not.

    Attributes:
        name (GameState): Enum that represents this game state
        clicked (boolean): whether the mouse has been clicked
        wager (int): Dollar amount the player would like to wager
        input (str): Keystrokes the user has entered
        buttons (Button, Button, Button): Continue, Correct, and Wrong buttons. Continue
            button is clicked after wager is entered. Correct and Wrong buttons are clicked
            after answer is given.
        timer (int): Milliseconds left to respond to question
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.DAILY_DOUBLE
        self.clicked = False
        self.wager = None
        self.input = ''
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))
        self.timer = 6000

    def startup(self, store):
        SoundEffects.play(2) # daily double sound
        self.store = store
        self.clicked = False
        self.wager = None
        self.input = ''
        self.timer = 6000

    def handle_event(self, event):
        """
        Reads user input for daily double wager and sets flag when mouse is clicked.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True
        elif event.type == pygame.KEYDOWN:
            # update user input when key is pressed
            if event.key == pygame.K_BACKSPACE:
                self.input = self.input[:-1] # delete last digit
            else:
                self.input += event.unicode

    def update(self, player_manager, elapsed_time):
        """Checks if the user has made a wager, reads the question, and counts down the time a
        player has left to answer. Also determines if the question was answered correctly or not.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            GameState: BOARD after question is answered, otherwise continues to return DAILY_DOUBLE
        """
        if TTS.is_busy():
            # question is still being read
            return GameState.DAILY_DOUBLE

        if self.wager is None:
            # Get wagered amount from user input when continue button is clicked
            if self.clicked and self.buttons.continue_button.was_clicked() and self.input.isdigit():
                self.wager = int(self.input)
                TTS.play_speech(self.store['clue']['answer']) # read question
        else:
            if self.timer <= 0:
                # Determine if player answered correctly based on which button was clicked
                if self.clicked:
                    player = player_manager.players[player_manager.control]
                    if self.buttons.correct_button.was_clicked():
                        # update player score
                        player.answer_question(True,self.wager)
                        return GameState.BOARD
                    if self.buttons.wrong_button.was_clicked():
                        # update player score
                        player.answer_question(False,self.wager)
                        return GameState.BOARD
            else:
                # Count down time left to answer
                self.timer -= elapsed_time
                if self.timer <= 0:
                    SoundEffects.play(1) # time's up
        self.clicked = False # reset flag
        return GameState.DAILY_DOUBLE

    def draw(self, screen):
        """Draws daily double wager screen, the question, or answer.

        Args:
            screen (Surface): Pygame surface where board will be drawn
        """
        # background color
        screen.fill(Colors.BLUE)

        width, height = screen.get_size()
        if self.wager is None:
            # Draw daily double text and continue button
            text = Font.number.render('DAILY DOUBLE', True, Colors.GOLD)
            rect = text.get_rect(center=(width/2, height/4))
            screen.blit(text,rect)
            self.buttons.continue_button.draw(screen, (width*1/2, height*3/4))
            # display wagered amount
            text = Font.number.render('$' + self.input, True, Colors.WHITE)
            rect = text.get_rect(center=(width/2, height/2))
            screen.blit(text,rect)
        elif self.timer <= 0:
            # draw answer
            text = self.store['clue']['question']
            draw_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
            # draw buttons
            self.buttons.correct_button.draw(screen, (width*1/4, height*3/4))
            self.buttons.wrong_button.draw(screen, (width*3/4, height*3/4))
        else:
            # draw clue
            text = self.store['clue']['answer']
            draw_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
