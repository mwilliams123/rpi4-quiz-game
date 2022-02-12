import pygame
from constants import GameState, Colors
from title import title_screen

# load pygame screen
pygame.init()
screen = pygame.display.set_mode((700,700))
game_state = GameState.TITLE

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

    if game_state is GameState.MAIN:
        screen.fill(Colors.BLUE)

    # Display screen
    pygame.display.flip()
        
pygame.quit()