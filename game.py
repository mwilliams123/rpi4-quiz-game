"""
Game Class
"""
import pygame
from constants import GameState
from util import display_score
from player_manager import PlayerManager

class Game():
    """
    Main game loop

    Responsible for executing the game loop, handling events, and switching
    between game states.
    """
    def __init__(self, screen, states, start_state=GameState.TITLE):
        """Initialize Game object

        Args:
            states (_type_): _description_
            start_state (_type_): _description_
        """
        self.screen = screen
        self.game_board = pygame.Surface((1000, 700))
        self.score_board = pygame.Surface((300, 700))
        self.clock = pygame.time.Clock()
        self.states = states
        self.state = states[start_state]
        self.player_manager = PlayerManager()
        self.font = pygame.font.Font('fonts/Anton-Regular.ttf', 60)

    def handle_events(self):
        """Handles events like mouse clicks, keyboard presses."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            self.state.handle_event(event)
        return False

    def change_state(self, next_state):
        """Changes and to the next game state and passes store state data."""
        print(next_state)
        store = self.state.store
        self.state = self.states[next_state]
        self.state.startup(store)

    def update(self, elapsed_time):
        """
        Calculates next game state

        elapsed_time: milliseconds since last frame
        """
        next_state = self.state.update(self.player_manager, elapsed_time)
        if next_state != self.state.name:
            self.change_state(next_state)


    def draw(self):
        """Draw frame"""
        if self.state.name in (GameState.TITLE, GameState.LOADING, GameState.INTRO):
            self.state.draw(self.screen)
        else:
            display_score(self.score_board, self.font, self.player_manager)
            self.screen.blit(self.score_board, (1000,0))
            self.state.draw(self.game_board)
            self.screen.blit(self.game_board, (0,0))


    def run(self):
        """
        Main game loop
        """
        while self.state != GameState.QUIT:
            elapsed_time = self.clock.tick()
            quit_pressed = self.handle_events()
            if quit_pressed:
                break
            self.draw()
            self.update(elapsed_time)
            # Display screen
            pygame.display.flip()
