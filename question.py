"""
Show question on screen and get player response
"""
from collections import namedtuple
import pygame
from constants import Colors, GameState
from util import SoundEffects, draw_text, Button, TTS, Font
from state import State

class Question(State):
    """Game state that handles presenting clues, waiting for players to ring in,
    and determining correctness of answers.

    Attributes:
        name (GameState): Enum that represents this game state
        show_answer (boolean): True if the timer has expired and answer should be shown
        rang_in (boolean): True if any player has rung in
        clicked (boolean): True if the mouse has been clicked
        buttons (Button, Button, Button): Continue, Correct, and Wrong buttons. Correct
            and Wrong buttons are shown after answer is given. Continue button is shown
            if no one rung in.
        timer (int): Milliseconds left for players to ring in
        """
    def __init__(self):
        super().__init__()
        self.name = GameState.QUESTION
        self.show_answer = False
        self.rang_in = False
        self.clicked = False
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))
        self.timer = 5000

    def startup(self, store, host):
        """Reads the question out loud and resets the timer.

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        TTS.play_speech(store['clue']['answer'])
        self.store = store
        self.clicked = False
        self.show_answer = False
        self.rang_in = False
        self.timer = 5000
        if host is not None:
            # send answer to host
            host.send(store['clue']['question'])

    def handle_event(self, event):
        """
        Sets flag when left mouse is clicked.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True

    def update(self, player_manager, elapsed_time, host):
        """Checks if players have rung in or time has expired for the question to be answered.
        Waits for user to click a button to return to board.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            (GameState): BOARD if question has been answered or continue button is clicked after
                no one rung in. Continues to return QUESTION otherwise.
        """
        if TTS.is_busy():
            # question is still being read
            return GameState.QUESTION
        if self.timer == 5000:
            # turn on light to let players know to ring in
            player_manager.green_light()

        if self.show_answer:
            # Check if buttons have been clicked to return to board
            if player_manager.rung_in is None:
                # continue button if no one rings in
                if self.clicked and self.buttons.continue_button.was_clicked():
                    return GameState.BOARD
            elif self.clicked:
                # Correct/incorrect button to indicate if player who rung in answered correctly
                if self.buttons.correct_button.was_clicked():
                    player_manager.update(True,self.store['clue']['value'])
                    return GameState.BOARD
                if self.buttons.wrong_button.was_clicked():
                    player_manager.update(False,self.store['clue']['value'])
                    return GameState.BOARD
        else:
            if player_manager.rung_in is None:
                # Decrement timer while waiting for players to ring in
                self.timer -= elapsed_time
                if self.timer <= 0:
                    # no one rung in
                    player_manager.reset()
                    SoundEffects.play(1) # time's up
                    if host is not None:
                        host.send("continue")
                        # wait for host to continue
                        resp = host.wait()
                        if resp:
                            print(resp)
                            return GameState.BOARD
                    else:
                        self.show_answer = True
            else:
                # player rang in, wait for response
                self.rang_in = True
                if player_manager.poll(elapsed_time):
                    # player has answered question
                    player_manager.reset()
                    if host is not None:
                        host.send("rangin")
                        resp = host.wait()
                        if resp == "True":
                            player_manager.update(True,self.store['clue']['value'])
                            return GameState.BOARD
                        if resp == "False":
                            player_manager.update(False,self.store['clue']['value'])
                            self.timer = 4999
                            return GameState.QUESTION
                    else:
                        self.show_answer = True
        self.clicked = False # reset flag
        return GameState.QUESTION

    def draw(self, screen):
        """
        Draws question or answer and buttons to screen.

        Args:
            screen (Surface): Pygame surface where board will be drawn
        """
        # background color
        screen.fill(Colors.BLUE)

        width, height = screen.get_size()
        if self.show_answer:
            # draw answer
            text = self.store['clue']['question']
            draw_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
            if self.rang_in:
                # draw correct/incorrect buttons
                self.buttons.correct_button.draw(screen, (width*1/4, height*3/4))
                self.buttons.wrong_button.draw(screen, (width*3/4, height*3/4))
            else:
                # draw continue button
                self.buttons.continue_button.draw(screen, (width*1/2, height*3/4))
        else:
            # draw question
            text = self.store['clue']['answer']
            draw_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
