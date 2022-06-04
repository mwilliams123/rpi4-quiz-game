"""
Util functions for score display.
"""
import pygame
from constants import Colors
from util import Font

class Score:
    """_summary_
    """

    def __init__(self, num_players) -> None:
        self.score_boxes = []
        self.screen = pygame.Surface((300, 700))
        width, height = self.screen.get_size()
        box_height = height / num_players
        for i in range(num_players):
            self.score_boxes.append((0, i*box_height, width, box_height)) # box for player's score
        self.clicked = False
        self.editing = None
        self.edit_text = ''

    def edit_score(self, player_manager):
        """Set score box to be edited."""
        y_pos = pygame.mouse.get_pos()[1]
        for i,box in enumerate(self.score_boxes):
            if y_pos >= box[1] and y_pos < box[1] + box[3]:
                # update score
                self.editing = i
                self.edit_text = str(player_manager.players[i].score)

    def update_score(self, event, player_manager):
        """Set score box to be edited."""
        if event.type == pygame.KEYDOWN:
            # update user input when key is pressed
            if event.key == pygame.K_BACKSPACE:
                self.edit_text = self.edit_text[:-1] # delete last digit
            elif event.key == pygame.K_RETURN:
                self.reset(player_manager)
            else:
                self.edit_text += event.unicode

    def reset(self, player_manager):
        """Call when change states."""
        if self.editing is not None:
            player_manager.players[self.editing].score = int(self.edit_text)
            self.editing = None

    def display_score(self, player_manager):
        """Draws the score board.

        Args:
            screen (Surface): Pygame surface where score board should be drawn
            player_manager (PlayerManager): Reference to manager that keeps track of players
        """
        # background color
        self.screen.fill(Colors.BLUE)

        # Draw score boxes stacked vertically - one box for each player
        for i, player in enumerate(player_manager.players):
            rect = self.score_boxes[i] # box for player's score
            active = player_manager.rung_in == player.number
            if self.editing == i:
                score = self.edit_text
                active = True
            else:
                score = player.score
            draw_score(self.screen, rect, i, score, player_manager.timer, active)
            if active:
                # draw white outline
                pygame.draw.rect(self.screen, Colors.WHITE, (5, rect[1]+5, rect[2]-10, rect[3]-10), 10)
            # draw box outline
            pygame.draw.rect(self.screen, Colors.BLACK, rect, 5)

def draw_score(screen, rect, player_number, score, timer, active):
    """Draws score and timer display for one player.

    Args:
        screen (Surface): screen (Surface): Pygame surface where score will be drawn
        rect (int, int, int, int): Tuple (x, y, width, height) representing box to draw score in
            (x,y) is pixel position of the top left corner. Width, height are dimensions of the box
        player (Player): Player object that contains score, timer info
        timer (int): Time in milliseconds left to answer question
    """
    # Draw player score amount
    text = Font.number.render('$' + str(score), True, Colors.WHITE)
    text_rect = text.get_rect(center=((rect[0] + rect[2])/2, rect[1] + rect[3]*2/3))
    screen.blit(text,text_rect)

    # Draw player identifier
    text = Font.number.render('Player ' + str(player_number + 1), True, Colors.WHITE)
    text_rect = text.get_rect(center=((rect[0] + rect[2])/2, rect[1] + rect[3]/4))
    screen.blit(text,text_rect)

    # Draw timer display - 9 rectangles colored red or black to indicate time remaining
    little_rect_width = rect[2]/9
    for i in range(9):
        color = Colors.BLACK
        if active:
            color = Colors.RED
            if (i < 5 and 4 - timer/1000 >= i) or (i >= 5 and timer/1000 + 4 < i):
                color = Colors.BLACK
        pygame.draw.rect(screen, color,
            (rect[0] + little_rect_width*i, rect[1] + rect[3] - 30, little_rect_width, 20))
        # draw border around rectangle
        pygame.draw.rect(screen, Colors.WHITE,
            (rect[0] + little_rect_width*i, rect[1] + rect[3] - 30, little_rect_width, 20), 2)
