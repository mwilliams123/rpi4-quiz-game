from constants import Colors, GameState
import pygame
from util import draw_text, draw_button

def draw_answer(screen, store, pm, mouse_click):
    screen.fill(Colors.BLUE)
    text = store['clue']['question']
    w, h = screen.get_size()
    draw_text(screen, text.upper(), store['fonts']['clue'], (100, 100, w-100, h-100))
    
    if pm.rung_in is None: 
        rect = draw_button(screen, 'Continue', (w*1/2, h*3/4))
        if mouse_click and rect.collidepoint(pygame.mouse.get_pos()):
            return GameState.BOARD
    else:
        # draw buttons
        correct_rect = draw_button(screen, 'Correct', (w*1/4, h*3/4))
        wrong_rect = draw_button(screen, 'Incorrect', (w*3/4, h*3/4))

        # determine if button clicked
        if mouse_click:
            if correct_rect.collidepoint(pygame.mouse.get_pos()):
                pm.update(True,store['clue']['value'])
                return GameState.BOARD
            if wrong_rect.collidepoint(pygame.mouse.get_pos()):
                pm.update(False,store['clue']['value'])
                return GameState.BOARD
    return GameState.ANSWER

def draw_question(screen, store):
    screen.fill(Colors.BLUE)
    text = store['clue']['answer']
    w, h = screen.get_size()
    draw_text(screen, text.upper(), store['fonts']['clue'], (100, 100, w-100, h-100))
