"""
Implement final jeopardy
"""
import pygame
from constants import Colors, GameState
from util import SoundEffects, draw_text, TTS, Fonts
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

    def handle_event(self, event):
        """
        Sets flag when left mouse is clicked.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True

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
        else:
            if not TTS.is_busy() and self.play_sound:
                # Wait for question to finish being read, then play final theme
                SoundEffects.play(3)
                self.play_sound = False
            elif not SoundEffects.is_busy():
                # When final theme finishes, show the answer
                self.show_answer = True

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
            final_rect = Fonts.NUMBER.render('Final Jeopardy', True, Colors.GOLD)
            rect = final_rect.get_rect(center=(width*1/2, height/4))
            screen.blit(final_rect,rect)

            # display category
            cat_rect = Fonts.NUMBER.render(text, True, Colors.WHITE)
            rect = cat_rect.get_rect(center = (width*1/2, height/2))
            screen.blit(cat_rect, rect)

            # display continue button
            text = clue['category']
            text_rect = Fonts.BUTTON.render('Continue', True, Colors.WHITE)
            rect = text_rect.get_rect(center=(width*1/2, height*3/4))
            screen.blit(text_rect,rect)
        else:
            # Display either the question or answer depending on if time has run out
            if self.show_answer:
                text = clue['question']
            else:
                text = clue['answer']
            draw_text(screen, text.upper(), Fonts.CLUE, (100, 100, width-100, height-100))
