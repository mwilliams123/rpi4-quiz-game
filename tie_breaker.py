"""
Show question on screen and get player response
"""
from collections import namedtuple
import requests
import pygame
import threading
from constants import Colors, GameState
from util import SoundEffects, display_text, Button, TTS, Font
from state import State

class TieBreaker(State):
    """Tie breaking round when scores are equal. First to ring in and guess correctly wins.

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
        self.name = GameState.TIE
        self.show_answer = False
        self.rang_in = False
        self.clicked = False
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))
        self.timer = 5000
        self.question = None
        self.thread = None
        self.winner = None
        self.loading = False
        self.show_category = True

    def startup(self, store, player_manager):
        """Reads the question out loud and resets the timer.

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        # fetch a clue
        self.store = store
        self.clicked = False
        self.tiebreaker(player_manager)

    def tiebreaker(self, player_manager):
        self.show_answer = False
        self.rang_in = False
        self.timer = 5000
        player_manager.reset()
        self.question = None
        self.show_category = True
        self.thread = threading.Thread(target=self.load_question)
        self.loading = True
        self.thread.start()

    def load_question(self):
        data = requests.get('http://mathnerd7.pythonanywhere.com/one')
        self.question = data.json()
        self.loading = False

    def play_question(self):
        TTS.play_speech(self.question['answer'])
        host = self.store['host']
        if host is not None:
            # send answer to host
            host.send("answer: " + self.question['question'])

    def handle_event(self, event):
        """
        Sets flag when left mouse is clicked.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True

    def update(self, player_manager, elapsed_time):
        """Checks if players have rung in or time has expired for the question to be answered.
        Waits for user to click a button to return to board.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            (GameState): BOARD if question has been answered or continue button is clicked after
                no one rung in. Continues to return QUESTION otherwise.
        """
        host = self.store['host']
        if TTS.is_busy() or self.loading:
            # question is still being read
            return GameState.TIE
        if not player_manager.green and not self.show_category:
            # turn on light to let players know to ring in
            player_manager.green_light(eligible=self.store['candidates'])
        if self.winner is not None:
            if self.clicked and self.buttons.continue_button.was_clicked():
                return GameState.HALL
        if self.show_category:
            if self.clicked and self.buttons.continue_button.was_clicked:
                self.play_question()
                self.show_category = False
        elif self.show_answer:
            # Check if buttons have been clicked to return to board
            if player_manager.rung_in is None:
                # continue button if no one rings in
                if self.clicked and self.buttons.continue_button.was_clicked():
                    # reload
                    self.tiebreaker(player_manager)
            elif self.clicked:
                # Correct/incorrect button to indicate if player who rung in answered correctly
                if self.buttons.correct_button.was_clicked():
                    self.winner = player_manager.rung_in
                if self.buttons.wrong_button.was_clicked():
                    self.tiebreaker(player_manager)
        else:
            if player_manager.rung_in is None:
                # Decrement timer while waiting for players to ring in
                self.timer -= elapsed_time
                if self.timer <= 0:
                    # no one rung in
                    if host is not None:
                        if not host.wait:
                            player_manager.reset()
                            SoundEffects.play(1) # time's up
                            host.send("continue")
                            host.wait = True
                        # wait for host to continue
                        if host.poll():
                            self.tiebreaker(player_manager)
                    else:
                        player_manager.reset()
                        SoundEffects.play(1) # time's up
                        self.show_answer = True
            else:
                # player rang in, wait for response
                if not self.rang_in:
                    if host is not None:
                        host.send("rangin")
                    self.rang_in = True

                if host is not None:
                    resp = host.poll()
                    if resp == "True":
                        self.winner = player_manager.rung_in
                        return GameState.TIE
                    if resp == "False":
                        self.timer = 5000
                        player_manager.second_chance()
                        return GameState.TIE

                if player_manager.timer > 0:
                    if player_manager.poll(elapsed_time):
                        # out of time
                        if host is None:
                            self.show_answer = True
                        else:
                            SoundEffects.play(1) # time's up
       
        self.clicked = False # reset flag
        return GameState.TIE

    def draw(self, screen):
        """
        Draws question or answer and buttons to screen.

        Args:
            screen (Surface): Pygame surface where board will be drawn
        """
        # background color
        screen.fill(Colors.BLUE)

        width, height = screen.get_size()
        if self.question is None:
            # loading
            display_text(screen, 'Loading...', Font.button, (100, 100, width-100, height-100))
        elif self.show_answer:
            # draw answer
            text = self.question['question']
            if self.rang_in:
                if self.winner is not None:
                    text = "Player " + str(self.winner + 1) + " wins!"
                    display_text(screen, text, Font.number, (100, 100, width-100, height-100))
                    self.buttons.continue_button.draw(screen, (width/2, height*3/4))
                    return
                else:
                    # draw correct/incorrect buttons
                    self.buttons.correct_button.draw(screen, (width*1/4, height*3/4))
                    self.buttons.wrong_button.draw(screen, (width*3/4, height*3/4))
            else:
                # draw continue button
                self.buttons.continue_button.draw(screen, (width*1/2, height*3/4))
            display_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
            
        elif self.show_category:
            # display category
            text = self.question['category']
            cat_rect = Font.number.render(text, True, Colors.WHITE)
            rect = cat_rect.get_rect(center = (width*1/2, height/2))
            screen.blit(cat_rect, rect)
            self.buttons.continue_button.draw(screen, (width*1/2, height*3/4))
        else:
            # draw question
            text = self.question['answer']
            display_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))

