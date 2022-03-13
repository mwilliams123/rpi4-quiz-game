import pygame
from board import draw_board
from constants import GameState
from player_manager import PlayerManager
from title import title_screen
from loading import load_data, loading_screen
from question import draw_question, draw_answer
from categories import show_categories
from util import load_fonts
#from hardware import green_light, ready

# load pygame screen
pygame.init()
screen = pygame.display.set_mode((1000,700))
game_state = GameState.TITLE
loading_thread = None
green = False
#ready()
store = {}
store['fonts'] = load_fonts()
pm = PlayerManager()
# Main loop
while game_state is not GameState.QUIT:
    mouse_click = False
    # Detect events like key presses
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = GameState.QUIT
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_click = True

    # Draw game
    if game_state is GameState.TITLE:
        game_state = title_screen(screen, mouse_click)
    if game_state is GameState.LOADING:
        if loading_thread is None:
            loading_thread = load_data()
        game_state, store = loading_screen(screen, loading_thread, store)
    if game_state is GameState.INTRO:
        game_state = show_categories(screen, store)
    if game_state is GameState.BOARD:
        game_state, store = draw_board(screen, mouse_click, store)
    if game_state is GameState.QUESTION:
        if not store['green']:
            pm.green_light()
            store['green'] = True
        game_state, store = pm.poll(store)
        draw_question(screen, store)
    if game_state is GameState.ANSWER:
        game_state = draw_answer(screen, store, pm, mouse_click)
    if game_state is GameState.FINAL:
        pass
        #game_state = final(screen, store)
    # Display screen
    pygame.display.flip()
        
pygame.quit()