"""
Implement final jeopardy
"""
import pygame
from constants import Colors
from util import draw_text, play_speech


def final(screen, store, player_manager, mouse_click):
    screen.fill(Colors.BLUE)
    width, height = screen.get_size()
    clue = store['data']['fj']
    text = ''
    elasped_time = store['clock'].tick()
    if not store['wagers']:
        text = clue['category']
        font = pygame.font.SysFont("arial", 40)
        text_rect = font.render('Continue', True, Colors.WHITE)
        rect = text_rect.get_rect(center=(width*1/2, height*3/4))
        screen.blit(text_rect,rect)

        if mouse_click and rect.collidepoint(pygame.mouse.get_pos()):
            store['wagers'] = True

        final_rect = store['fonts']['number'].render('Final Jeopardy', True, Colors.GOLD)
        rect = final_rect.get_rect(center=(width*1/2, height/4))
        screen.blit(final_rect,rect)
    else:
        if store['read'] == 0:
            # draw
            store['read'] = 1
        elif store['read'] == 1:
            play_speech(clue['answer'])
            store['read'] = 2
        elif store['read'] == 2:
            player_manager.sound_effects(3)
            store['read'] = 3
        else:
            store['timer'] = store['timer'] - elasped_time
        if store['timer'] < 0:
            text = clue['question']
        else:
            text = clue['answer']
    draw_text(screen, text.upper(), store['fonts']['clue'], (100, 100, width-100, height-100))
