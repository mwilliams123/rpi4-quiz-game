"""
Main Game Looop
"""
import pygame
from pygame.time import Clock
from board import draw_board
from constants import GameState
from player_manager import PlayerManager
from title import title_screen
from loading import load_data, loading_screen
from question import draw_question, draw_answer
from categories import show_categories
from util import load_fonts, play_speech
from score import display_score
from final import final
from daily_double import daily_double

# load pygame screen
# pylint: disable=no-member
pygame.init()
screen = pygame.display.set_mode((1300,700))
game_board = pygame.Surface((1000, 700))
score = pygame.Surface((300, 700))
game_state = GameState.TITLE
loading_thread = None
store = {
    'wagers': False,
    'timer': 35000,
    'clock': Clock(),
    'read': 0
}
store['fonts'] = load_fonts()
player_manager = PlayerManager()
# Main loop
while game_state is not GameState.QUIT:
    mouse_click = False
    # Detect events like key presses
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = GameState.QUIT
            else:
                player_manager.update_input(event)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_click = True

    # Draw game
    if game_state is GameState.TITLE:
        game_state = title_screen(game_board, mouse_click)
    if game_state is GameState.LOADING:
        if loading_thread is None:
            loading_thread = load_data()
        game_state, store = loading_screen(game_board, loading_thread, store)
    if game_state is GameState.INTRO:
        game_state = show_categories(screen, store)
    if game_state is GameState.BOARD:
        game_state, store = draw_board(game_board, mouse_click, store, player_manager)
    if game_state is GameState.QUESTION:
        if not store['green']:
            store['green'] = True
            player_manager.read_text = True
        elif player_manager.read_text:
            text = store['clue']['answer']
            play_speech(text)
            player_manager.read_text = False
            player_manager.clock.tick()
            player_manager.green_light()
        else:
            game_state, store = player_manager.poll(store)
        draw_question(game_board, store)
    if game_state is GameState.DAILY_DOUBLE:
        game_state = daily_double(game_board, store, player_manager, mouse_click)
    if game_state is GameState.ANSWER:
        game_state = draw_answer(game_board, store, player_manager, mouse_click)
    if game_state is GameState.FINAL:
        final(game_board, store, player_manager, mouse_click)
    if game_state != GameState.TITLE and game_state != GameState.LOADING:
        display_score(score, store, player_manager)
    screen.blit(game_board, (0,0))
    screen.blit(score, (1000,0))
    # Display screen
    pygame.display.flip()

pygame.quit()
