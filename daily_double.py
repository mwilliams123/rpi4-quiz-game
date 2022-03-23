"""
Implement daily double
"""
import pygame
from constants import GameState, Colors
from util import draw_text, play_speech, draw_button
from question import draw_question

def daily_double(screen, store, player_manager, mouse_click):
    width, height = screen.get_size()
    elasped_time = player_manager.clock.tick()
    if player_manager.dd_status == 0:
        player_manager.sound_effects(2)
        player_manager.dd_status += 1
    if player_manager.dd_wager is None:
        screen.fill(Colors.BLUE)
        font = store['fonts']['number']
        text = font.render('DAILY DOUBLE', True, Colors.GOLD)
        rect = text.get_rect(center=(width/2, height/4))
        screen.blit(text,rect)
        font = pygame.font.SysFont("arial", 40)
        text_rect = font.render('Continue', True, Colors.WHITE)
        rect = text_rect.get_rect(center=(width*1/2, height*3/4))
        screen.blit(text_rect,rect)

        if mouse_click and rect.collidepoint(pygame.mouse.get_pos()) and player_manager.input.isdigit():
            player_manager.dd_wager = int(player_manager.input)
            player_manager.timer = 6000
            player_manager.play_sound = True

        # display wager
        text = font.render('$' + player_manager.input, True, Colors.WHITE)
        rect = text.get_rect(center=(width/2, height/2))
        screen.blit(text,rect)
        return GameState.DAILY_DOUBLE
    else:
        if player_manager.timer < 0:
            if player_manager.play_sound:
                player_manager.sound_effects(1)
                player_manager.play_sound = False
            screen.fill(Colors.BLUE)
            text = store['clue']['question']
            width, height = screen.get_size()
            draw_text(screen, text.upper(), store['fonts']['clue'], (100, 100, width-100, height-100))
            # draw buttons
            correct_rect = draw_button(screen, 'Correct', (width*1/4, height*3/4))
            wrong_rect = draw_button(screen, 'Incorrect', (width*3/4, height*3/4))

            # determine if button clicked
            if mouse_click:
                player = player_manager.players[player_manager.control]
                if correct_rect.collidepoint(pygame.mouse.get_pos()):
                    player.answer_question(True,player_manager.dd_wager)
                    player_manager.dd_status = 0
                    player_manager.dd_wager = None
                    return GameState.BOARD
                if wrong_rect.collidepoint(pygame.mouse.get_pos()):
                    player_manager.dd_status = 0
                    player.answer_question(False,player_manager.dd_wager)
                    player_manager.dd_wager = None
                    return GameState.BOARD
        else:
            if player_manager.dd_status == 1:
                player_manager.dd_status += 1
            elif player_manager.dd_status == 2:
                play_speech(store['clue']['answer'])
                player_manager.dd_status += 1
            elif player_manager.dd_status == 3:
                player_manager.dd_status += 1
            else:
                player_manager.timer -= elasped_time
            draw_question(screen, store)
    return GameState.DAILY_DOUBLE
