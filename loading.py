"""
Load questions from external API.
"""
import threading
import requests
from constants import GameState, Colors
from util import Font
from state import State
from server import Server

class LoadingScreen(State):
    """Game State that draws loading screen and loads questions.

    Attributes:
        name (GameState): Enum that represents this game state
        text (Surface): Pygame surface where loading text is drawn
        data (dict of Any: dict): Nested dictionary of questions. Dictionary is indexed
            by round (1,2, or 'fj'), and then indexed again by category (str). Each category
            contains a list of question objects.
        thread (Thread): a thread used to load data from the API
    """
    def __init__(self):
        super().__init__()
        self.name = GameState.LOADING
        self.text = Font.button.render("Loading...", True, Colors.WHITE)
        self.data = {}
        self.thread = None

    def startup(self, store, player_manager):
        """
        Starts a new thread to fetch questions.

        Args:
            store (dict of str: Any): Dictionary of persistent data passed from state to state
        """
        self.store = store
        self.thread = threading.Thread(target=self.fetch)
        self.thread.start()
        if self.store['hosted']:
            self.store['host'] = Server()
        else:
            self.store['host'] = None

    def fetch(self):
        """Fetches questions from the API and formats them into rounds."""
        data = requests.get('http://mathnerd7.pythonanywhere.com/api')
        data_json = data.json()
        self.load_round(data_json['clues'][0], 0)
        self.load_round(data_json['clues'][1], 1) # double jeopardy round
        # final jeopardy
        self.data['fj'] = data_json['fj']

    def update(self, player_manager, elapsed_time):
        """Checks if data has finished loading from the API.

        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
            GameState: Returns INTRO game state when questions have finished loading,
                otherwise returns LOADING state.
        """
        host = self.store['host']
        # wait for host connection
        if host is not None and not host.is_connected():
            host.poll_for_connection()

        # check if loading thread has exited
        if not self.thread.is_alive():
            self.store['data'] = self.data
            self.store['round'] = 0
            if host is None or host.is_connected():
                return GameState.INTRO
        return GameState.LOADING

    def draw(self, screen):
        """
        Draws Loading text on simple background.

        Args:
            screen (Surface): Pygame display where frame will be drawn
        """
        # background color
        screen.fill(Colors.BLACK)

        # draw loading text at top of screen
        width, _ = screen.get_size()
        text_rect = self.text.get_rect(center=(width/2, 30))
        screen.blit(self.text, text_rect)

    def load_round(self, clues, round_):
        """Organizes questions into a dictionary indexed by round and category.

        Args:
            clues (list of list): 2d array containing questions.
            round_ (int): The questions' round number (1 or 2).
        """
        self.data[round_] = {}
        cats = []
        for clue in clues[0]:
            cats.append(clue['category'] )
        for value in clues:
            for i, clue in enumerate(value):
                category = cats[i]
                if category not in self.data[round_]:
                    self.data[round_][category] = []
                self.data[round_][category].append(clue)
