import pygame

# color definitions
BLUE = (6, 12, 233)

# load pygame screen
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
pygame.quit()