"""
Template for implementing Game State classes.

Each game state must have an update() function for handling game logic
that returns the next game state, and a draw() function that draws the
current frame to the screen.

Game states may optionally implement their own startup() function to be
called once when a state is loaded, or a handle_event() function that
handles user input such as mouse clicks and keyboard presses.
"""
from collections import namedtuple
import pygame
from util import Button
class State():
    """
    Abstract class for game states.

    Attributes:
        store (dict of str: Any): Dictionary of data that should be persistent and
            transfered from state to state
    """
    def __init__(self):
        self.store = {}

    def startup(self, store, player_manager):
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

# pylint: disable=W0223
class InputState(State):
    """Abstract class for game states that require user input.

    Attributes:
        clicked (boolean): whether the mouse has been clicked
        input (str): Keystrokes the user has entered
        buttons (Button, Button, Button): Continue, Correct, and Wrong buttons. Continue
            button is clicked after wager is entered. Correct and Wrong buttons are clicked
            after answer is given.
    """
    def __init__(self):
        super().__init__()
        self.clicked = False
        self.input = ''
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))

    def handle_event(self, event):
        """
        Sets flag when left mouse is clicked. Captures user keyboard input.

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

    def answer_question(self, player):
        """Checks to see if correct/incorrect buttons were clicked and updates player score.

        Args:
            player (Player): The player who has answered the question

        Returns:
            boolean: True if a button was clicked, false otherwise.
        """
        if self.clicked:
            wager = int(self.input)
            if self.buttons.correct_button.was_clicked():
                player.answer_question(True, wager)
                self.input = ''
                return True
            if self.buttons.wrong_button.was_clicked():
                player.answer_question(False, wager)
                self.input = ''
                return True
        return False

    def draw_buttons(self, screen):
        """Draws correct/incorrect buttons on bottom of screen.

        Args:
            screen (Surface): Pygame surface where board will be drawn
        """
        width, height = screen.get_size()
        self.buttons.correct_button.draw(screen, (width*1/4, height*3/4))
        self.buttons.wrong_button.draw(screen, (width*3/4, height*3/4))
