from constants import Colors
from util import draw_text
import pygame

def final(screen, store, mouse_click):
    screen.fill(Colors.BLUE)
    w, h = screen.get_size()
    clue = store['data']['fj']
    text = ''
    if not store['wagers']:
        text = clue['category']
        font = pygame.font.SysFont("arial", 40)
        text_rect = font.render('Continue', True, Colors.WHITE)
        rect = text_rect.get_rect(center=(w*1/2, h*3/4))
        screen.blit(text_rect,rect)
        if mouse_click and rect.collidepoint(pygame.mouse.get_pos()):
            store['wagers'] = True
    else:
        et = store['clock'].tick()
        store['timer'] = store['timer'] - et
        if store['timer'] < 0:
            text = clue['question']
        else:
            text = clue['answer']
    draw_text(screen, text.upper(), store['fonts']['clue'], (100, 100, w-100, h-100))
        
    
