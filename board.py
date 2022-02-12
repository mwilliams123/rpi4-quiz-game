
from constants import Colors, GameState
import pygame


def draw_number(screen, num, rect):
    font = pygame.font.SysFont("arial", 60)
    text = font.render(str(num), True, Colors.WHITE)
    text_rect = pygame.Rect(rect)
    screen.blit(text,text_rect)

def draw_board(screen, mouse_click):
    screen.fill(Colors.BLUE)
    
    # draw grid
    width, height = screen.get_size()
    v_lines = range(0,width, width//6)
    h_lines = range(0,height, height//6+1)
    for i in v_lines:
        pygame.draw.line(screen, Colors.WHITE, (i, 0), (i, height))
    for i in h_lines:
        pygame.draw.line(screen, Colors.WHITE, (0, i), (width, i))
    for i,x in enumerate(v_lines):
        for j,y in enumerate(h_lines):
            if j != 0:
                draw_number(screen, j*200, (x,y, x+width//6, y+height//6))

    # draw categories

    # get Q from pos of mouse
    if mouse_click:
        return GameState.QUESTION
    return GameState.BOARD