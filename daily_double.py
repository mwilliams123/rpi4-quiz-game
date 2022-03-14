from constants import GameState, Colors
from util import draw_text
from question import draw_question
import pygame
from util import draw_button, draw_text

def daily_double(screen, store, pm, mouse_click):
    w, h = screen.get_size()
    et = pm.clock.tick()
    if pm.dd_wager is None:
        screen.fill(Colors.BLUE)
        font = store['fonts']['number']
        text = font.render('DAILY DOUBLE', True, Colors.GOLD)
        rect = text.get_rect(center=(w/2, h/4))
        screen.blit(text,rect)
        
        font = pygame.font.SysFont("arial", 40)
        text_rect = font.render('Continue', True, Colors.WHITE)
        rect = text_rect.get_rect(center=(w*1/2, h*3/4))
        screen.blit(text_rect,rect)
        
        if mouse_click and rect.collidepoint(pygame.mouse.get_pos()) and pm.input.isdigit():
            pm.dd_wager = int(pm.input)
            pm.timer = 10000
            pm.play_sound = True
            
        # display wager
        text = font.render('$' + pm.input, True, Colors.WHITE)
        rect = text.get_rect(center=(w/2, h/2))
        screen.blit(text,rect)
        return GameState.DAILY_DOUBLE
    else:
        pm.timer -= et
        if pm.timer < 0:
            if pm.play_sound:
                pm.sound_effects(1)
                pm.play_sound = False
            screen.fill(Colors.BLUE)
            text = store['clue']['question']
            w, h = screen.get_size()
            draw_text(screen, text.upper(), store['fonts']['clue'], (100, 100, w-100, h-100))
            # draw buttons
            correct_rect = draw_button(screen, 'Correct', (w*1/4, h*3/4))
            wrong_rect = draw_button(screen, 'Incorrect', (w*3/4, h*3/4))

            # determine if button clicked
            if mouse_click:
                player = pm.players[pm.control]
                if correct_rect.collidepoint(pygame.mouse.get_pos()):
                    player.answer_question(True,pm.dd_wager)
                    return GameState.BOARD
                if wrong_rect.collidepoint(pygame.mouse.get_pos()):
                    player.answer_question(False,pm.dd_wager)
                    return GameState.BOARD
        else:
            draw_question(screen, store)
    return GameState.DAILY_DOUBLE
