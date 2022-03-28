"""
Load questions from API
"""
import threading
from unicodedata import category
import requests
import pygame
from constants import GameState, Colors
from util import Fonts
from state import State

class LoadingScreen(State):
    """Draws loading screen and loads questions."""
    def __init__(self):
        super(LoadingScreen, self).__init__()
        self.name = GameState.LOADING
        self.text = Fonts.BUTTON.render("Loading...", True, Colors.WHITE)
        width, _ = pygame.display.get_surface().get_size()
        self.text_rect = self.text.get_rect(center=(width/2, 30))
        self.data = {}
        self.thread = None

    def startup(self, store):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        store: a dict passed from state to state
        """
        self.store = store
        self.thread = threading.Thread(target=self.fetch)
        self.thread.start()

    def fetch(self):
        # fetch data
        round_ = requests.get('http://mathnerd7.pythonanywhere.com/api')
        data_json = round_.json()
        self.load_round(data_json['clues'][0], 0)
        self.load_round(data_json['clues'][1], 1) # double jeopardy round
        # final jeopardy
        self.data['fj'] = data_json['fj']
# 
    def update(self, player_manager, elapsed_time):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        # check if loading thread has exited
        if not self.thread.is_alive():
            self.store['data'] = self.data
            self.store['round'] = 0
            return GameState.INTRO
            #return GameState.INTRO
        return GameState.LOADING

    def draw(self, screen):
        """
        Draw everything to the screen.
        """
        # background color
        screen.fill(Colors.BLACK)

        # draw start button
        screen.blit(self.text,self.text_rect)

    def load_round(self, clues, round_):
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
