from constants import GameState, Colors
from util import play_speech, draw_text
import time
import pygame

def show_categories(screen, store):
    play_speech("The categories are")
    time.sleep(1)
    w, h = screen.get_size()
    r = store['round']
    print(store['data'][r])
    for cat in store['data'][r]:
        screen.fill(Colors.BLUE)
        font = store['fonts']['number']
        draw_text(screen, cat, font, (100, 100, w-100, h-100))
        pygame.display.flip()
        play_speech(cat)
        comments = store['data'][r][cat][0]['comments']
        if comments != '-':
            play_speech(comments)
        time.sleep(0.25)
        
    return GameState.BOARD