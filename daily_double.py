"""
Implement Daily Double
"""
from constants import GameState, Colors
from util import TTS, SoundEffects, display_text, Font
from state import InputState

class DailyDouble(InputState):
    """Handles the implementation of Daily Double questions.

    Allows a player to enter a wager, then displays a question on screen. After
    a timer runs out, shows the answer and prompts the user to click if the reponse
    was correct or not.

    Attributes:
        name (GameState): Enum that represents this game state
        wager (int): Dollar amount the player would like to wager
        timer (int): Milliseconds left to respond to question
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.DAILY_DOUBLE
        self.wager = None
        self.timer = 6000

    def startup(self, store):
        SoundEffects.play(2) # daily double sound
        self.store = store
        self.clicked = False
        self.wager = None
        self.timer = 6000

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
                    if self.answer_question(player):
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
            display_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
            # draw correct/incorrect buttons
            self.draw_buttons(screen)
        else:
            # draw clue
            text = self.store['clue']['answer']
            display_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
