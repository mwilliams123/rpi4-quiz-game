"""
Display category intro
"""
import time
import pygame
from constants import GameState, Colors
from util import play_speech, draw_text


def show_categories(screen, store):
    """
    Iterate through categories and explain each one
    """
    play_speech("The categories are")
    time.sleep(1)
    width, height = screen.get_size()
    round_ = store['round']
    for cat in store['data'][round_]:
        screen.fill(Colors.BLUE)
        font = store['fonts']['number']
        draw_text(screen, cat, font, (100, 100, width-100, height-100))
        pygame.display.flip()
        play_speech(cat)
        comments = store['data'][round_][cat][0]['comments']
        if comments != '-':
            play_speech(comments)
        time.sleep(0.25)
    return GameState.BOARD
