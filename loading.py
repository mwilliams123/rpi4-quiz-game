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
        #player_manager.zero_scores()

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
            if self.check_data():
                self.store['data'] = self.data
            else:
                # fetch again
                self.thread = threading.Thread(target=self.fetch)
                self.thread.start()
                return GameState.LOADING
            self.store['round'] = 0
            if host is None or host.is_connected():
                return GameState.BOARD
        return GameState.LOADING

    def check_data(self):
        """Returns true if data is valid
        """
        if 'fj' not in self.data or not self.check_clue(self.data['fj']):
            print("Bad final jeopardy: " + str(self.data['fj']))
            return False
        return self.check_round(0) and self.check_round(1)

    def check_round(self, round_):
        if round_ not in self.data or len(self.data[round_].keys()) < 6:
            print("Not enough categories for round " + str(round_))
            return False
        for cat in self.data[round_]:
            if not self.check_category(self.data[round_][cat], round_):
                return False
        return True

    def check_category(self, category, round_):
        values = set([x*(round_+1) for x in [200,400,600,800,1000]])
        daily_double = 0
        if len(category) < 5:
            print("Not enought clues: " + str(category))
            return False
        for clue in category:
            if not self.check_clue(clue):
                return False
            if clue['daily_double'] == 1:
                daily_double += 1
            else:
                if clue['value'] not in values:
                    print('Clue has bad value: ' + str(clue))
                    return False
                values.discard(clue['value'])
        if len(values) == 0:
            return True
        if len(values) == 1 and daily_double == 1:
            return True
        print("Clues have wrong values: " + str(category))
        return False

    def check_clue(self, clue):
        try:
            return len(clue['category']) > 0 and len(clue['answer'])>0 and len(clue['question'])>0
        except KeyError:
            print('Bad clue: ' + str(clue))
            return False


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
