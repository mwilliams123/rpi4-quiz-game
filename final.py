"""
Implement final jeopardy
"""

from constants import Colors, GameState
from util import SoundEffects, draw_text, TTS, Font
from state import InputState

class Final(InputState):
    """Handles the implementation of Final Jeopardy.

    Shows the Final Jeopardy Category and waits for players to make wagers.
    Displays the question, gives players 30 seconds to answer, then shows
    the correct response.

    Attributes:
        name (GameState): Enum that represents this game state
        show_answer (boolean): True if the timer has expired and answer should be shown
        wait_for_wagers (boolean): True if players have not entered wagers yet
        play_sound (boolean): True if final theme should be played
        winner (int): id number of the player who won the game
        players_left (list of Player): List of players whose final scores haven't been
            updated yet.
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.FINAL
        self.show_answer = False
        self.wait_for_wagers = True
        self.play_sound = False
        self.winner = None
        self.players_left = []
        self.hosted = False

    def startup(self, store, host):
        self.store = store
        if host is not None:
            # send answer to host
            self.hosted = True

    def update(self, player_manager, elapsed_time, host):
        """Checks if players have entered wagers, reads question, and plays final theme.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            GameState: FINAL game state
        """
        clue = self.store['data']['fj']
        if self.wait_for_wagers:
            # Wait until continue is clicked, then present question
            if self.clicked:
                self.wait_for_wagers = False
                TTS.play_speech(clue['answer'])
                self.play_sound = True
        elif not self.show_answer:
            if not TTS.is_busy() and self.play_sound:
                # Wait for question to finish being read, then play final theme
                SoundEffects.play(3)
                self.play_sound = False
            elif not SoundEffects.is_busy():
                # When final theme finishes, show the answer
                if host is not None:
                    host.send("Answer: " + clue['question'])
                self.show_answer = True
                self.players_left = player_manager.sort_players()
        if self.show_answer and self.winner is None:
            player = self.players_left[0]
            if self.answer_question(player):
                self.players_left.pop(0)
            if len(self.players_left) <= 0:
                # show winner
                self.winner = player_manager.get_winner()
        self.clicked = False
        return GameState.FINAL

    def draw(self, screen):
        """
        Draws final jeopardy wager screen, question, or answer.

        Args:
            screen (Surface): Pygame surface where board will be drawn
        """
        # background color
        screen.fill(Colors.BLUE)

        clue = self.store['data']['fj']
        width, height = screen.get_size()
        if self.wait_for_wagers:
            # display 'Final Jeopardy'
            final_rect = Font.number.render('Final Jeopardy', True, Colors.GOLD)
            rect = final_rect.get_rect(center=(width*1/2, height/4))
            screen.blit(final_rect,rect)

            # display category
            text = clue['category']
            cat_rect = Font.number.render(text, True, Colors.WHITE)
            rect = cat_rect.get_rect(center = (width*1/2, height/2))
            screen.blit(cat_rect, rect)

            # display continue button
            text_rect = Font.button.render('Continue', True, Colors.WHITE)
            rect = text_rect.get_rect(center=(width*1/2, height*3/4))
            screen.blit(text_rect,rect)
        else:
            # Display either the question or answer depending on if time has run out
            if self.show_answer:
                if self.winner is not None:
                    text = "Player " + str(self.winner + 1) + " wins!"
                    draw_text(screen, text, Font.number, (100, 100, width-100, height-100))
                else:
                    # draw answer
                    if not self.hosted:
                        text = clue['question']
                        draw_text(screen, text.upper(), Font.clue, (100, 0, width-100, height/3))
                    player = self.players_left[0].number
                    text = "Player " + str(player + 1) + " wager:"
                    draw_text(screen, text, Font.number, (100, height/3, width-100, height/2))
                    # draw wagered amount
                    text = Font.number.render('$' + self.input, True, Colors.WHITE)
                    rect = text.get_rect(center=(width/2, height*3/5))
                    screen.blit(text,rect)
                    # draw correct/incorrect buttons
                    self.draw_buttons(screen)
            else:
                # draw clue
                text = clue['answer']
                draw_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
