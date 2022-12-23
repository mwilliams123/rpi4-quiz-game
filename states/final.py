"""
Implement final jeopardy
"""

from util.constants import Colors, GameState
from util.util import Button, SoundEffects, display_text, TTS, Font
from states.state import InputState

class Final(InputState):
    """Handles the implementation of Final Jeopardy.

    Shows the Final Jeopardy Category and waits for players to make wagers.
    Displays the question, gives players 30 seconds to answer, then shows
    the correct response.

    Attributes:
        show_answer (boolean): True if the timer has expired and answer should be shown
        wait_for_wagers (boolean): True if players have not entered wagers yet
        play_sound (boolean): True if final theme should be played
        winner (int): id number of the player who won the game
        players_left (list of Player): List of players whose final scores haven't been
            updated yet.
    """
    def __init__(self):
        super().__init__()
        self.show_answer = False
        self.wait_for_wagers = True
        self.play_sound = False
        self.winner = None
        self.players_left = []
        self.return_button = Button('Continue')

    def play_final(self, player_manager):
        """Play final jeopardy theme."""
        if not TTS.is_busy() and self.play_sound:
            # Wait for question to finish being read, then play final theme
            SoundEffects.play(3)
            self.play_sound = False
        elif not SoundEffects.is_busy():
            # When final theme finishes, show the answer
            host = self.store['host']
            if host is not None:
                host.send("Answer: " + self.store['data']['fj']['question'])
            self.show_answer = True
            self.players_left = player_manager.sort_players()

    def update(self, player_manager, elapsed_time):
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
            self.play_final(player_manager)

        if self.show_answer and self.winner is None:
            if len(self.players_left) > 0:
                player = self.players_left[0]
                if self.answer_question(player):
                    self.players_left.pop(0)

            if len(self.players_left) == 0:
                # show winner
                candidates = player_manager.get_winner()
                if len(candidates) == 1:
                    self.winner = candidates[0]
                else:
                    # tie breaker
                    self.store['candidates'] = candidates
                    return GameState.TIE

        if self.winner is not None:
            if self.clicked and self.return_button.was_clicked():
                return GameState.HALL
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
                    text = "Player " + str(self.winner.number + 1) + " wins!"
                    display_text(screen, text, Font.number, (100, 100, width-100, height-100))
                    self.return_button.draw(screen, (width/2, height*3/4))
                else:
                    # draw answer
                    if self.store['host'] is None:
                        text = clue['question']
                        display_text(screen, text.upper(), Font.clue, (100, 0, width-100, height/3))
                    player = self.players_left[0].number
                    text = "Player " + str(player + 1) + " wager:"
                    display_text(screen, text, Font.number, (100, height/3, width-100, height/2))
                    # draw wagered amount
                    text = Font.number.render('$' + self.input, True, Colors.WHITE)
                    rect = text.get_rect(center=(width/2, height*3/5))
                    screen.blit(text,rect)
                    # draw correct/incorrect buttons
                    self.draw_buttons(screen)
            else:
                # draw clue
                text = clue['answer']
                display_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
