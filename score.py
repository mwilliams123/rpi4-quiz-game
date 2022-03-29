"""
Util functions for score display.
"""
import pygame
from constants import Colors
from util import Fonts

def draw_score(screen, rect, player):
    """Draws score and timer display for one player.

    Args:
        screen (Surface): screen (Surface): Pygame surface where score will be drawn
        rect (int, int, int, int): Tuple (x, y, width, height) representing box to draw score in
            (x,y) is pixel position of the top left corner. Width, height are dimensions of the box
        player (Player): Player object that contains score, timer info
    """
    # Draw player score amount
    text = Fonts.NUMBER.render('$' + str(player.score), True, Colors.WHITE)
    text_rect = text.get_rect(center=((rect[0] + rect[2])/2, rect[1] + rect[3]*2/3))
    screen.blit(text,text_rect)

    # Draw player identifier
    text = Fonts.NUMBER.render('Player ' + str(player.number + 1), True, Colors.WHITE)
    text_rect = text.get_rect(center=((rect[0] + rect[2])/2, rect[1] + rect[3]/4))
    screen.blit(text,text_rect)

    # Draw timer display - 9 rectangles colored red or black to indicate time remaining
    little_rect_width = rect[2]/9
    for i in range(9):
        color = Colors.BLACK
        if player.active:
            color = Colors.RED
            if (i < 5 and 4 - player.timer/1000 > i) or (i >= 5 and player.timer/1000 + 4 < i):
                color = Colors.BLACK
        pygame.draw.rect(screen, color,
            (rect[0] + little_rect_width*i, rect[1] + rect[3] - 30, little_rect_width, 20))
        # draw border around rectangle
        pygame.draw.rect(screen, Colors.WHITE,
            (rect[0] + little_rect_width*i, rect[1] + rect[3] - 30, little_rect_width, 20), 2)

def display_score(screen, player_manager):
    """Draws the score board.

    Args:
        screen (Surface): Pygame surface where score board should be drawn
        player_manager (PlayerManager): Reference to manager that keeps track of players
    """
    # background color
    screen.fill(Colors.BLUE)

    # Draw score boxes stacked vertically - one box for each player
    width, height = screen.get_size()
    box_height = height / len(player_manager.players)
    for i, player in enumerate(player_manager.players):
        rect = (0, i*height, width, box_height) # box for player's score
        draw_score(screen, rect, player)
        if player.active:
            # draw white outline
            pygame.draw.rect(screen, Colors.WHITE, (5, i*height+5, width-10, box_height-10), 10)
        # draw box outline
        pygame.draw.rect(screen, Colors.BLACK, rect, 5)
    