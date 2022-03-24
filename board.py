"""
Draw game board & clues
"""
import pygame
from constants import Colors, GameState
from util import draw_text
from state import State

class Board(State):
    """
    Parent class for individual game states to inherit from.
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.BOARD
        self.number_font = pygame.font.Font('fonts/Anton-Regular.ttf', 60)
        self.font = pygame.font.Font('fonts/Anton-Regular.ttf', 24)
        self.clicked = False
        self.grid = ([], [])

    def handle_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True

    def startup(self, store):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        store: a dict passed from state to state
        """
        self.store = store
        self.clicked = False

    def update(self, player_manager, elapsed_time):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        # check if all clues gone from board
        round_ = self.store['round']
        if not self.check_clues_left(self.store['data'][round_]):
            # move to next round
            self.store['round'] = round_ + 1
            if self.store['round'] >= 2:
                return GameState.FINAL
            player_manager.update_control()
            return GameState.INTRO
        # get Q from pos of mouse
        if self.clicked:
            h_lines, v_lines = self.grid
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
            cat = list(self.store['data'][round_].keys())[i-1]
            clues = self.store['data'][round_][cat]
            clue = clues[j-2]
            if clue is not None:
                self.store['clue'] = clue
                clues[j-2] = None # remove clue from board
                self.store['green'] = False
                if clue['daily_double'] == 1:
                    return GameState.DAILY_DOUBLE
                return GameState.QUESTION
        return GameState.BOARD

    def draw(self, screen):
        """Draw game board"""
        screen.fill(Colors.BLUE)
        round_ = self.store['round']
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
                if j != 0 and list(self.store['data'][round_].values())[i][j-1] is not None:
                    self.draw_number(screen, j*200*(round_+1),
                                (x_pos,y_pos, width//6, height//6),
                                self.number_font)
        self.grid = (h_lines, v_lines)

        # draw categories
        x_pos = 0
        for cat in self.store['data'][round_]:
            draw_text(screen, cat, self.font, (x_pos + 5,0, x_pos + width//6 - 5, height//6))
            x_pos += width//6 + 1

    def check_clues_left(self, clues):
        clues_left = False
        for cat in clues:
            for clue in clues[cat]:
                if clue is not None:
                    clues_left = True
        return clues_left

    def draw_number(self, screen, num, rect, font):
        text = font.render('$' + str(num), True, Colors.GOLD)
        text_rect = text.get_rect(center=(rect[0] + rect[2]/2, rect[1] + rect[3]/2))
        screen.blit(text,text_rect)
