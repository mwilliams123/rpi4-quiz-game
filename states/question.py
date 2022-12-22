"""
Show question on screen and get player response
"""
from collections import namedtuple
from util.constants import Colors, GameState
from util.util import SoundEffects, display_text, Button, TTS, Font
from states.state import State

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
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))
        self.timer = 5000
        self.show_score = True

    def startup(self, store, player_manager):
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
        host = self.store['host']
        player_manager.reset()
        player_manager.log_clue()
        if host is not None:
            # send answer to host
            host.send("answer: " + store['clue']['question'])

    def wait_for_continue(self, player_manager):
        """Check if buttons have been clicked to return to board."""
        if not self.rang_in:
            # continue button if no one rings in
            if self.clicked and self.buttons.continue_button.was_clicked():
                return GameState.BOARD
        elif self.clicked:
            # Correct/incorrect button to indicate if player who rung in answered correctly
            if self.buttons.correct_button.was_clicked():
                player_manager.log_question_stats()
                player_manager.update(True,self.store['clue']['value'])
                return GameState.BOARD
            if self.buttons.wrong_button.was_clicked():
                player_manager.log_question_stats()
                player_manager.update(False,self.store['clue']['value'])
                return GameState.BOARD
        return None
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
        if TTS.is_busy():
            # question is still being read
            return GameState.QUESTION
        if not player_manager.green:
            # turn on light to let players know to ring in
            player_manager.green_light()

        if self.show_answer:
            next_state = self.wait_for_continue(player_manager)
            if next_state is not None:
                return next_state
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
                        resp = host.poll()
                        if resp:
                            player_manager.triple_stumpers += 1
                            player_manager.log_question_stats()
                            return GameState.BOARD
                    else:
                        player_manager.triple_stumpers += 1
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
                        player_manager.log_question_stats()
                        player_manager.reset()
                        player_manager.update(True,self.store['clue']['value'])
                        return GameState.BOARD
                    if resp == "False":
                        self.timer = 5000
                        player_manager.second_chance()
                        player_manager.update(False,self.store['clue']['value'])
                        self.rang_in = False
                        return GameState.QUESTION

                if player_manager.timer > 0:
                    if player_manager.poll(elapsed_time):
                        # out of time
                        if host is None:
                            self.show_answer = True
                        else:
                            SoundEffects.play(1) # time's up

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
            display_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
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
            display_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
