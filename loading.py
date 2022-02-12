import threading
import requests
import pygame
from constants import GameState, Colors

def fetch():
    r = requests.get('http://mathnerd7.pythonanywhere.com/api')
    return r.json()

def load_data():
    t = threading.Thread(target=fetch)
    t.start()
    return t

def loading_screen(screen, thread):
    # Render loading screen
    screen.fill(Colors.BLACK)
    font = pygame.font.SysFont("arial", 60)
    text = font.render("Loading...", True, Colors.WHITE)
    w, _ = pygame.display.get_surface().get_size()
    text_rect = text.get_rect(center=(w/2, 30))
    screen.blit(text,text_rect)

    # check if loading thread has exited
    if not thread.is_alive():
        return GameState.MAIN
    return GameState.LOADING
