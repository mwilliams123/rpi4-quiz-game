"""
Draw game board & clue values.
"""
import pygame
from util.constants import Colors, GameState
from util.util import display_text, Font
from states.state import State

class Board(State):
    """
    Class that represents the Game Board.

    Displays the categories and shows the clue values for remaining
    clues on the board. Allows users to click on the next clue.

    Attributes:
        name (GameState): Enum that represents this game state
        clicked (boolean): Whether the mouse has been clicked
        grid (list of int, list of int): Tuple (vertical_lines, horizontal_lines) of the
            lines used to draw the game board. Each line is represented by an integer that
            is the pixel row (for horizontal lines) or pixel column (vertical lines) the
            line is centered on.
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.BOARD
        self.grid = ([], [])
        self.show_score = True

    def startup(self, store, player_manager):
        """
        Turns on light of player who has control

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        self.store = store
        player_manager.reset()
        player_manager.show_control()

    def update(self, player_manager, elapsed_time):
        """Checks if a clue was clicked on. Moves to the next round if no clues left.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            GameState: QUESTION or DAILY_DOUBLE if a valid question was clicked on. Returns
                INTRO or FINAL to advance to next round if all clues are gone. Otherwise,
                continues to return BOARD.
        """
        # check if all clues gone from board
        round_ = self.store['round']
        if not self.check_clues_left(round_):
            # move to next round
            self.store['round'] = round_ + 1
            if self.store['round'] >= 2:
                return GameState.FINAL
            player_manager.update_control()
            return GameState.INTRO

        # check if any clues were clicked on
        if self.clicked:
            self.clicked = False # reset flag
            horizontal_lines, vertical_lines = self.grid
            pos = pygame.mouse.get_pos()
            i = 0 # game grid column that was clicked
            while i < len(vertical_lines):
                if pos[0] < vertical_lines[i]:
                    break
                i += 1
            j = 0 # game grid row that was clicked
            while j < len(horizontal_lines):
                if pos[1] < horizontal_lines[j]:
                    break
                j += 1
            if j < 2:
                return GameState.BOARD
            # Find which clue was clicked based on grid row, col
            category = list(self.store['data'][round_].keys())[i-1]
            clues = self.store['data'][round_][category]
            clue = clues[j-2]

            # check if clicked clue is still on board
            if clue is not None:
                self.store['clue'] = clue
                clues[j-2] = None # remove clue from board
                if clue['daily_double'] == 1:
                    return GameState.DAILY_DOUBLE
                return GameState.QUESTION
        return GameState.BOARD

    def draw(self, screen):
        """Draws game board and clue values, skipping exhausted clues.

        The game board consists of 6 rows and 6 columns. Each column contains the
        clues for one category. The first row is the category names, and rows 2-6
        contain clue value amounts.

        Args:
            screen (Surface): Pygame surface where game board will be drawn
        """
        # background color
        screen.fill(Colors.BLUE)

        # draw 6x6 grid on screen
        width, height = screen.get_size()
        step = width//6+1
        vertical_lines = range(0, width + step, step) # vertical lines
        horizontal_lines = range(0,height, height//6+1) # horizonal lines
        for i in vertical_lines:
            pygame.draw.line(screen, Colors.BLACK, (i, 0), (i, height), 5)
        for i in horizontal_lines:
            pygame.draw.line(screen, Colors.BLACK, (0, i), (width, i), 5)
        self.grid = (horizontal_lines, vertical_lines)

        # draw clues values on board
        round_ = self.store['round']
        for i, x_pos in enumerate(vertical_lines):
            for j, y_pos in enumerate(horizontal_lines):
                if j>0 and i<6 and list(self.store['data'][round_].values())[i][j-1] is not None:
                    draw_number(screen, j*200*(round_+1), (x_pos,y_pos, width//6, height//6))

        # draw categories
        x_pos = 0
        for category in self.store['data'][round_]:
            display_text(screen, category, Font.category, (x_pos + 5, 0, x_pos + width//6 - 5,
                      height//6))
            x_pos += width//6 + 1

    def check_clues_left(self, round_):
        """Returns True if any clues are still left on board, False otherwise.

        Args:
            rount_ (int): Current round number (1 or 2).
        """
        clues = self.store['data'][round_]
        clues_left = False
        for category in clues:
            for clue in clues[category]:
                if clue is not None:
                    clues_left = True
        return clues_left

def draw_number(screen, num, rect):
    """Draws the clue value on the board.

    Args:
        screen (Surface): Pygame surface where board will be drawn
        num (int): Dollar value of clue
        rect (int, int, int, int): Rectangle (x,y, width, height) the clue value will be
            centered inside. (x,y) is the pixel (relative to screen) of the top left
            corner of the rectangle. Width and height are the dimensions.
    """
    text = Font.number.render('$' + str(num), True, Colors.GOLD)
    text_shadow = Font.number.render('$' + str(num), True, Colors.BLACK)
    center_rect = (rect[0] + rect[2]/2, rect[1] + rect[3]/2)
    offset_rect = (center_rect[0]+2, center_rect[1]+2)
    # draw text shadow
    text_rect = text.get_rect(center=offset_rect)
    screen.blit(text_shadow,text_rect)
    # draw text
    text_rect = text.get_rect(center=center_rect)
    screen.blit(text,text_rect)
