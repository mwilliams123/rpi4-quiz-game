"""
Implement final jeopardy
"""
from collections import namedtuple
import pygame
from constants import Colors, GameState
from util import SoundEffects, draw_text, TTS, Font, Button
from state import State

class Final(State):
    """Handles the implementation of Final Jeopardy.

    Shows the Final Jeopardy Category and waits for players to make wagers.
    Displays the question, gives players 30 seconds to answer, then shows
    the correct response.

    Attributes:
        name (GameState): Enum that represents this game state
        show_answer (boolean): True if the timer has expired and answer should be shown
        clicked (boolean): whether the mouse has been clicked
        wait_for_wagers (boolean): True if players have not entered wagers yet
        play_sound (boolean): True if final theme should be played
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.FINAL
        self.show_answer = False
        self.clicked = False
        self.wait_for_wagers = True
        self.play_sound = False
        self.input = ''
        self.index = 0
        ButtonList = namedtuple('ButtonsList',['continue_button', 'correct_button', 'wrong_button'])
        self.buttons = ButtonList(Button('Continue'), Button('Correct'), Button('Incorrect'))
        self.winner = None
        self.players_by_score = []

    def handle_event(self, event):
        """
        Sets flag when left mouse is clicked.

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
            if not TTS.is_busy() and self.play_sound:
                # Wait for question to finish being read, then play final theme
                SoundEffects.play(3)
                self.play_sound = False
            elif not SoundEffects.is_busy():
                # When final theme finishes, show the answer
                self.show_answer = True
                self.players_by_score = player_manager.sort_players()
        if self.show_answer and self.winner is None:
            player = self.players_by_score[self.index]
            if self.clicked:
                wager = int(self.input)
                if self.buttons.correct_button.was_clicked():
                    player.answer_question(True, wager)
                    self.input = ''
                    self.index += 1
                if self.buttons.wrong_button.was_clicked():
                    player.answer_question(False, wager)
                    self.input = ''
                    self.index += 1
            if self.index >= len(self.players_by_score):
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
                    text = clue['question']
                    draw_text(screen, text.upper(), Font.clue, (100, 0, width-100, height/3))
                    player = self.players_by_score[self.index].number
                    text = "Player " + str(player + 1) + " wager:"
                    draw_text(screen, text, Font.number, (100, height/3, width-100, height/2))
                    # draw wagered amount
                    text = Font.number.render('$' + self.input, True, Colors.WHITE)
                    rect = text.get_rect(center=(width/2, height*3/5))
                    screen.blit(text,rect)
                    # draw correct/incorrect buttons
                    self.buttons.correct_button.draw(screen, (width*1/4, height*3/4))
                    self.buttons.wrong_button.draw(screen, (width*3/4, height*3/4))
            else:
                # draw clue
                text = clue['answer']
                draw_text(screen, text.upper(), Font.clue, (100, 100, width-100, height-100))
