import pygame
from constants import GameState, Colors


def title_screen(screen, mouse_click):
    # background color
    screen.fill(Colors.BLACK)

    # draw start button
    font = pygame.font.SysFont("arial", 60)
    text = font.render("Play", True, Colors.WHITE)
    w, h = pygame.display.get_surface().get_size()
    text_rect = text.get_rect(center=(w/2, h/2))
    screen.blit(text,text_rect)

    # determine if start button clicked
    if mouse_click and text_rect.collidepoint(pygame.mouse.get_pos()):
        return GameState.LOADING

    return GameState.TITLE