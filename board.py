"""
Draw game board & clues
"""
import pygame
from constants import Colors, GameState
from util import draw_text

def check_clues_left(clues):
    clues_left = False
    for cat in clues:
        for clue in clues[cat]:
            if clue is not None:
                clues_left = True
    return clues_left

def draw_number(screen, num, rect, font):
    text = font.render('$' + str(num), True, Colors.GOLD)
    text_rect = text.get_rect(center=(rect[0] + rect[2]/2, rect[1] + rect[3]/2))
    screen.blit(text,text_rect)

def draw_board(screen, mouse_click, store, player_manager):
    screen.fill(Colors.BLUE)
    round_ = store['round']

    # check if all clues gone from board
    if not check_clues_left(store['data'][round_]):
        # move to next round
        store['round'] = round_ + 1
        if store['round'] >= 2:
            return GameState.FINAL, store
        player_manager.update_control()
        return GameState.INTRO, store

    # draw grid
    width, height = screen.get_size()
    v_lines = range(0,width, width//6+1)
    h_lines = range(0,height, height//6+1)
    for i in v_lines:
        pygame.draw.line(screen, Colors.BLACK, (i, 0), (i, height), 5)
    for i in h_lines:
        pygame.draw.line(screen, Colors.BLACK, (0, i), (width, i), 5)
    for i, x_pos in enumerate(v_lines):
        for j, y_pos in enumerate(h_lines):
            if j != 0 and list(store['data'][round_].values())[i][j-1] is not None:
                draw_number(screen, j*200*(round_+1), (x_pos,y_pos, width//6, height//6), store['fonts']['number'])

    # draw categories
    x_pos = 0
    for cat in store['data'][round_]:
        draw_text(screen, cat, store['fonts']['category'], (x_pos + 5,0, x_pos + width//6 - 5, height//6))
        x_pos += width//6 + 1
    # get Q from pos of mouse
    if mouse_click:
        pos = pygame.mouse.get_pos()
        i = 0
        while i < len(v_lines):
            if pos[0] < v_lines[i]:
                break
            i += 1
        j = 0
        while j < len(h_lines):
            if pos[1] < h_lines[j]:
                break
            j += 1
        cat = list(store['data'][round_].keys())[i-1]
        clues = store['data'][round_][cat]
        clue = clues[j-2]
        if clue is not None:
            store['clue'] = clue
            clues[j-2] = None # remove clue from board
            store['green'] = False
            if clue['daily_double'] == 1:
                return GameState.DAILY_DOUBLE, store
            return GameState.QUESTION, store
    return GameState.BOARD, store
