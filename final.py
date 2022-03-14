from constants import Colors
from util import draw_text, play_speech
import pygame

def final(screen, store, mouse_click):
    screen.fill(Colors.BLUE)
    w, h = screen.get_size()
    clue = store['data']['fj']
    text = ''
    et = store['clock'].tick()
    if not store['wagers']:
        text = clue['category']
        font = pygame.font.SysFont("arial", 40)
        text_rect = font.render('Continue', True, Colors.WHITE)
        rect = text_rect.get_rect(center=(w*1/2, h*3/4))
        screen.blit(text_rect,rect)
        
        if mouse_click and rect.collidepoint(pygame.mouse.get_pos()):
            store['wagers'] = True
            
        final_rect = store['fonts']['number'].render('Final Jeopardy', True, Colors.GOLD)
        rect = final_rect.get_rect(center=(w*1/2, h/4))
        screen.blit(final_rect,rect)
    else:
        if store['read'] == 0:
            # draw
            store['read'] = 1
        elif store['read'] == 1:
            play_speech(clue['answer'])
            store['read'] = 2
        elif store['read'] == 2:
            store['read'] = 3
        else:
            store['timer'] = store['timer'] - et
        if store['timer'] < 0:
            text = clue['question']
        else:
            text = clue['answer']
    draw_text(screen, text.upper(), store['fonts']['clue'], (100, 100, w-100, h-100))
        
    
