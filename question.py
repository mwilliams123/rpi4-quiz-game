"""
Display question
"""
import pygame
from constants import Colors, GameState
from util import draw_text, draw_button

def draw_answer(screen, store, player_manager, mouse_click):
    screen.fill(Colors.BLUE)
    text = store['clue']['question']
    width, height = screen.get_size()
    draw_text(screen, text.upper(), store['fonts']['clue'], (100, 100, width-100, height-100))

    if player_manager.rung_in is None:
        rect = draw_button(screen, 'Continue', (width*1/2, height*3/4))
        if mouse_click and rect.collidepoint(pygame.mouse.get_pos()):
            return GameState.BOARD
    else:
        # draw buttons
        correct_rect = draw_button(screen, 'Correct', (width*1/4, height*3/4))
        wrong_rect = draw_button(screen, 'Incorrect', (width*3/4, height*3/4))

        # determine if button clicked
        if mouse_click:
            if correct_rect.collidepoint(pygame.mouse.get_pos()):
                player_manager.update(True,store['clue']['value'])
                return GameState.BOARD
            if wrong_rect.collidepoint(pygame.mouse.get_pos()):
                player_manager.update(False,store['clue']['value'])
                return GameState.BOARD
    return GameState.ANSWER

def draw_question(screen, store):
    screen.fill(Colors.BLUE)
    text = store['clue']['answer']
    width, height = screen.get_size()
    draw_text(screen, text.upper(), store['fonts']['clue'], (100, 100, width-100, height-100))
