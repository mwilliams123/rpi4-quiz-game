from glob import glob
import threading
import requests
import pygame
from constants import GameState, Colors

data = {}

def load_round(clues, r):
    global data
    data[r] = {}
    for value in clues:
        for clue in value:
            if clue['category'] not in data[r]:
                data[r][clue['category']] = []
            data[r][clue['category']].append(clue)

def fetch():
    global data
    r = requests.get('http://mathnerd7.pythonanywhere.com/api')
    data_json = r.json()
    load_round(data_json['clues'][0], 0)
    load_round(data_json['clues'][1], 1) # double jeopardy round
    # final jeopardy
    data['fj'] = data_json['fj']


def load_data():
    t = threading.Thread(target=fetch)
    t.start()
    return t

def loading_screen(screen, thread, store = {}):
    global data
    # Render loading screen
    screen.fill(Colors.BLACK)
    font = pygame.font.SysFont("arial", 60)
    text = font.render("Loading...", True, Colors.WHITE)
    w, _ = pygame.display.get_surface().get_size()
    text_rect = text.get_rect(center=(w/2, 30))
    screen.blit(text,text_rect)

    # check if loading thread has exited
    if not thread.is_alive():
        store['data'] = data
        store['round'] = 0
        return GameState.INTRO, store
    return GameState.LOADING, store
