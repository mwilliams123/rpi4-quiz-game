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
from util.util import Button, Font, SoundEffects
from util.constants import Colors

class State():
    """
    Abstract class for game states.

    Attributes:
        name (GameState): Enum that represents this game state
        store (dict of str: Any): Dictionary of data that should be persistent and
            transfered from state to state
    """
    def __init__(self):
        self.store = {}
        self.show_score = False
        self.clicked = False
        self.name = None

    def set_name(self, name):
        """Set title for a game state."""
        self.name = name
    def startup(self, store, _player_manager):
        """
        Executes once immediately after a state is transitioned into.

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        self.clicked = False
        self.store = store

    def handle_event(self, event):
        """
        Controls logic for dealing with user input.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True

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

#pylint: disable=W0223
class QuestionState(State):
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
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))
        self.show_score = True
        self.timer = 5000
        self.show_answer = False
        self.rang_in = False

    def reset(self, player_manager):
        """Reset after question."""
        self.clicked = False
        self.show_answer = False
        self.rang_in = False
        self.timer = 5000
        player_manager.reset()

    def draw_buttons(self, screen):
        """Draws correct/incorrect buttons on bottom of screen.

        Args:
            screen (Surface): Pygame surface where board will be drawn
        """
        width, height = screen.get_size()
        if self.rang_in:
            # draw correct/incorrect buttons
            self.buttons.correct_button.draw(screen, (width*1/4, height*3/4))
            self.buttons.wrong_button.draw(screen, (width*3/4, height*3/4))
        else:
            # draw continue button
            self.buttons.continue_button.draw(screen, (width*1/2, height*3/4))

    def wait_for_host(self, player_manager):
        """Wait for host to click continue after time out."""
        host = self.store['host']
        if not host.wait:
            player_manager.reset()
            SoundEffects.play(1) # time's up
            host.send("continue")
            host.wait = True
        # wait for host to continue
        return host.poll()
    def wait_for_response(self, player_manager, elapsed_time):
        """Wait for response from player who range in."""
        host = self.store['host']
        if not self.rang_in:
            if host is not None:
                host.send("rangin")
            self.rang_in = True

        if player_manager.timer > 0:
            if player_manager.poll(elapsed_time):
                # out of time
                if host is None:
                    self.show_answer = True
                else:
                    SoundEffects.play(1) # time's up

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
        self.input = ''
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))
        self.correct = False
        self.show_score = True

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
            try:
                wager = int(self.input)
            except ValueError:
                return False
            if self.buttons.correct_button.was_clicked():
                player.answer_question(True, wager)
                self.input = ''
                self.correct = True
                return True
            if self.buttons.wrong_button.was_clicked():
                player.answer_question(False, wager)
                self.input = ''
                self.correct = False
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

    def draw_input(self, screen):
        """Draws wagered amount on screen.

        Args:
            screen (Surface): Pygame surface where board will be drawn
        """
        width, height = screen.get_size()
        text = Font.number.render('$' + self.input, True, Colors.WHITE)
        rect = text.get_rect(center=(width/2, height*3/5))
        screen.blit(text,rect)
