from glob import glob
import threading
import requests
import pygame
from constants import GameState, Colors

data = {}
def fetch():
    global data
    r = requests.get('http://mathnerd7.pythonanywhere.com/api')
    data_json = r.json()
    round1 = data_json['clues'][0]
    for value in round1:
        for clue in value:
            if clue['category'] not in data:
                data[clue['category']] = []
            data[clue['category']].append(clue)

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
        print(data)
        return GameState.BOARD, store
    return GameState.LOADING, store
