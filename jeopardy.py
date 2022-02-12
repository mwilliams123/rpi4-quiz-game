import pygame
from constants import GameState, Colors

# load pygame screen
pygame.init()
screen = pygame.display.set_mode((700,700))
game_state = GameState.TITLE

# Main loop
while game_state is not GameState.QUIT:
    
    # Detect events like key presses
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = GameState.QUIT
                
    # Draw game
    if game_state is GameState.TITLE:
        screen.fill(Colors.BLUE)
    
    # Display screen
    pygame.display.flip()
        
pygame.quit()