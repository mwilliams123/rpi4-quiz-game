"""
Show question on screen and get player response
"""
import threading
import requests
from util.constants import Colors, GameState
from util.util import SoundEffects, display_text, TTS, Font
from states.state import QuestionState

class TieBreaker(QuestionState):
    """Tie breaking round when scores are equal. First to ring in and guess correctly wins.

    Attributes:
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
        self.question = None
        self.thread = None
        self.winner = None
        self.show_category = True

    def startup(self, store, player_manager):
        """Reads the question out loud and resets the timer.

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        # fetch a clue
        super().startup(store, player_manager)
        self.tiebreaker(player_manager)

    def tiebreaker(self, player_manager):
        """Load new question and reset player eligibility to ring in."""
        self.reset(player_manager)
        self.question = None
        self.show_category = True
        self.thread = threading.Thread(target=self.load_question)
        self.thread.start()

    def load_question(self):
        """Fetch a tiebreaker question."""
        data = requests.get('http://mathnerd7.pythonanywhere.com/one',  timeout=60)
        self.question = data.json()

    def play_question(self):
        """Read question aloud."""
        TTS.play_speech(self.question['answer'])
        host = self.store['host']
        if host is not None:
            # send answer to host
            host.send("answer: " + self.question['question'])

    def determine_winner(self, player_manager):
        """Wait for input to determine if player won."""
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

    def wait_for_ring_in(self, player_manager, elapsed_time):
        """Decrement timer while waiting for players to ring in."""
        self.timer -= elapsed_time
        if self.timer <= 0:
            # no one rung in
            host = self.store['host']
            if host is not None:
                if self.wait_for_host(player_manager):
                    self.tiebreaker(player_manager)
            else:
                player_manager.reset()
                SoundEffects.play(1) # time's up
                self.show_answer = True

    def update(self, player_manager, elapsed_time):
        """Checks if players have rung in or time has expired for the question to be answered.
        Waits for user to click a button to return to board.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            (GameState): End of game HALL state if question has been answered correctly.
                Continues to return TIE otherwise.
        """
        if TTS.is_busy() or self.question is None:
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
            self.determine_winner(player_manager)
        else:
            if player_manager.rung_in is None:
                self.wait_for_ring_in(player_manager,elapsed_time)
            else:
                self.wait_for_response(player_manager,elapsed_time)
                host = self.store['host']
                if host is not None:
                    resp = host.poll()
                    if resp == "True":
                        self.winner = player_manager.rung_in
                        return GameState.TIE
                    if resp == "False":
                        self.timer = 5000
                        player_manager.second_chance()
                        return GameState.TIE

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
            self.draw_buttons(screen)
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
