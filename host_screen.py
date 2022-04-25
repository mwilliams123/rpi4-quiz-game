"""
Show answer on screen and let host indicate if answered correctly
"""
from collections import namedtuple
import pygame
from constants import Colors
from util import draw_text, Button,  Font

class Host():
    """Game state that handles presenting clues, waiting for players to ring in,
    and determining correctness of answers.

    Attributes:
        rang_in (boolean): True if any player has rung in
        timer_expired (boolean): True if question timer expired and no one rung in
        clicked (boolean): True if the mouse has been clicked
        buttons (Button, Button, Button): Continue, Correct, and Wrong buttons. Correct
            and Wrong buttons are shown after answer is given. Continue button is shown
            if no one rung in.
        timer (int): Milliseconds left for players to ring in
        """
    def __init__(self):
        self.rang_in = False
        self.timer_expired = False
        self.clicked = False
        self.correct = False
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))

    def startup(self):
        """Reset state."""
        self.clicked = False
        self.timer_expired = False
        self.rang_in = False

    def handle_event(self):
        """
        Watches for escape key press and sets flag when left mouse is clicked.
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Exit game if escape key is pressed
                    return True
            # pass along event to be handled by current state
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.clicked = True
        return False

    def update(self):
        """Checks if players have rung in or time has expired for the question to be answered.
        Waits for host to click a button to return to board."""
        # Check if buttons have been clicked to return to board
        if self.clicked:
            if self.rang_in:
                # Correct/incorrect button to indicate if player who rung in answered correctly
                if self.buttons.correct_button.was_clicked():
                    self.correct = True
                    return True
                if self.buttons.wrong_button.was_clicked():
                    self.correct = False
                    return True

            elif self.timer_expired:
                # continue button if no one rings in
                if self.clicked and self.buttons.continue_button.was_clicked():
                    self.correct = True
                    return True
        self.clicked = False
        return False

    def draw(self, screen, text):
        """
        Draws answer and buttons to screen.

        Args:
            screen (Surface): Pygame surface where board will be drawn
            test (str): The answer to de drawn
        """
        # background color
        screen.fill(Colors.BLUE)

        width, height = screen.get_size()
        # draw answer
        draw_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
        if self.rang_in:
            # draw correct/incorrect buttons
            self.buttons.correct_button.draw(screen, (width*1/4, height*3/4))
            self.buttons.wrong_button.draw(screen, (width*3/4, height*3/4))
        elif self.timer_expired:
            # draw continue button
            self.buttons.continue_button.draw(screen, (width*1/2, height*3/4))
