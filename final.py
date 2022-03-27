"""
Implement final jeopardy
"""
import pygame
from constants import Colors, GameState
from util import SoundEffects, draw_text, TTS, Fonts
from state import State

class Final(State):
    """Draws question"""
    def __init__(self):
        super().__init__()
        self.name = GameState.FINAL
        self.show_answer = False
        self.clicked = False
        self.wait_for_wagers = True
        self.read_clue = True
        self.play_sound = True

    def handle_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True

    def update(self, player_manager, elapsed_time):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        if self.clicked:
            self.wait_for_wagers = False
        return GameState.FINAL

    def draw(self, screen):
        """
        Draw everything to the screen.
        """
        # background color
        screen.fill(Colors.BLUE)
        width, height = screen.get_size()
        clue = self.store['data']['fj']
        if self.wait_for_wagers:
            text = clue['category']
            text_rect = Fonts.BUTTON.render('Continue', True, Colors.WHITE)
            rect = text_rect.get_rect(center=(width*1/2, height*3/4))
            screen.blit(text_rect,rect)
            final_rect = Fonts.NUMBER.render('Final Jeopardy', True, Colors.GOLD)
            rect = final_rect.get_rect(center=(width*1/2, height/4))
            screen.blit(final_rect,rect)
        elif not self.show_answer:
            if self.read_clue:
                TTS.play_speech(clue['answer'])
                self.read_clue = False
            if self.play_sound:
                SoundEffects.play(3)
                self.play_sound = False
            draw_text(screen, clue['answer'].upper(), Fonts.CLUE, (100, 100, width-100, height-100))
        else:
            draw_text(screen, clue['question'].upper(), Fonts.CLUE, (100, 100, width-100, height-100))
