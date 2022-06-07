"""
Launches the game and executes main game logic.

Usage Example:
    screen = pygame.display.set_mode()
    game = Game(screen, {1: State(), 2: State()})
    game.run()
"""
import pygame
from constants import GameState
from score import Score
from player_manager import PlayerManager

class Game():
    """
    Class that contains the main game logic.

    Responsible for executing the game loop, handling events, and switching
    between game states.

    Attributes:
        screen (Surface): Pygame display where game will be drawn
        game_board (Surface): Pygame surface where game board will be drawn
        score_board (Surface): Pygame surface where score will be drawn
        clock (Clock): Pygame clock object that tracks time
        states (dict of GameSate: State): Dictionary of all possible game states
        state (State): The game's current state
        player_manager (PlayerManager): A reference to the PlayerManager object
            that keeps track of players
    """
    def __init__(self, screen, states, start_state=GameState.TITLE):
        """Initializes Game Object

        Args:
            screen (Surface): Pygame display where game will be drawn
            states (dict of GameSate: State): Dictionary of all possible game states
            start_state (GameState, optional): name of state the game enters on launch.
                Defaults to GameState.TITLE.
        """
        self.screen = screen
        self.game_board = pygame.Surface((1000, 700))
        self.clock = pygame.time.Clock()
        self.states = states
        self.state = states[start_state]
        self.player_manager = PlayerManager()
        self.score_board = Score(len(self.player_manager.players))

    def handle_events(self):
        """Handles events like mouse clicks, keyboard presses.

        Returns:
            boolean: True if game should exit, false otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Exit game if escape key is pressed
                    return True
            if self.state.name == GameState.BOARD:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and pygame.mouse.get_pos()[0] > 1000:
                    self.score_board.edit_score(self.player_manager)
                    return False
                self.score_board.update_score(event, self.player_manager)
            # pass along event to be handled by current state
            self.state.handle_event(event)
        return False

    def change_state(self, next_state):
        """Changes state to the next game state and passes along persistent data."""
        store = self.state.store
        self.state = self.states[next_state]
        self.state.startup(store, self.player_manager)
        self.score_board.reset(self.player_manager)

    def update(self, elapsed_time):
        """Handles game logic and determines what the next game state should be

        Args:
            elapsed_time (int): Milliseconds passed since the last time update() was called.
        """
        next_state = self.state.update(self.player_manager, elapsed_time)
        if next_state != self.state.name:
            self.change_state(next_state)

    def draw(self):
        """Draws the current frame to the screen."""
        if self.state.name in (GameState.TITLE, GameState.LOADING, GameState.INTRO, GameState.HALL):
            self.state.draw(self.screen)
        else:
            # draw score board
            self.score_board.display_score(self.player_manager)
            self.screen.blit(self.score_board.screen, (1000,0))
            # draw the game board
            self.state.draw(self.game_board)
            self.screen.blit(self.game_board, (0,0))

    def run(self):
        """
        Runs main game loop.

        Each iteration will check for user inputs, render the game on screen,
        and update the game state. Loop will run until game is quit.
        """
        while True:
            quit_pressed = self.handle_events()
            if quit_pressed:
                break
            self.draw()
            elapsed_time = self.clock.tick()
            self.update(elapsed_time)
            # Display screen
            pygame.display.flip()

        if 'host' in self.state.store and self.state.store['host'] is not None:
            self.state.store['host'].close()
            print("Host server closed.")
