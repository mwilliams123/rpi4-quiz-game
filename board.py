
from constants import Colors, GameState
import pygame

def draw_number(screen, num, rect):
    font = pygame.font.SysFont("arial", 60)
    text = font.render(str(num), True, Colors.WHITE)
    text_rect = pygame.Rect(rect)
    screen.blit(text,text_rect)

def blit_text(screen, text, pos, width):
    font = pygame.font.SysFont("arial", 24)
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width = width
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, Colors.WHITE)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            screen.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def draw_board(screen, mouse_click, store):
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
    x = 0
    for cat in store['data']:
        blit_text(screen, cat, (x,0), width//6)
        x += width//6
    # get Q from pos of mouse
    if mouse_click:
        pos = pygame.mouse.get_pos()
        print(pos)
        for i in range(7):
            if pos[0] < v_lines[i]:
                break
        for j in range(6):
            if pos[1] < h_lines[j]:
                break
        print(i,j)
        clues = list(store['data'].values())[i-1]
        clue = clues[j-2]
        store['clue'] = clue['answer']
        print(clue)
        return GameState.QUESTION, store
    return GameState.BOARD, store