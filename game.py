import pygame
from constants import GameState, Colors
from title import title_screen
from loading import load_data, loading_screen

# load pygame screen
pygame.init()
screen = pygame.display.set_mode((700,700))
game_state = GameState.TITLE
loading_thread = None

# Main loop
while game_state is not GameState.QUIT:

    mouse_click = False
    # Detect events like key presses
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = GameState.QUIT
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click = True


    # Draw game
    if game_state is GameState.TITLE:
        game_state = title_screen(screen, mouse_click)
    if game_state is GameState.LOADING:
        if loading_thread is None:
            loading_thread = load_data()
        game_state = loading_screen(screen, loading_thread)
    if game_state is GameState.MAIN:
        screen.fill(Colors.BLUE)

    # Display screen
    pygame.display.flip()
        
pygame.quit()