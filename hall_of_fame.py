import pickle
import pygame
from state import State
from constants import Colors, GameState
from util import Button, Font

class Hall(State):
    def __init__(self):
        super().__init__()
        self.name = GameState.HALL
        self.scores = []
        self.input = ''
        self.continue_button = Button('Return')
        self.enter_button = Button('Enter')
        self.new_entry = False
        self.clicked = False
        self.place = None

    def startup(self, store, player_manager):
        try:
            file = open('scores', 'rb')
            self.scores = pickle.load(file)
            file.close()
        except Exception as error:
            print(error)
            self.scores = []
        if 'round' in store and store['round'] >= 2:
            self.new_entry = True
        self.place = None

    def handle_event(self, event):
        """
        Sets flag when left mouse is clicked. Captures user keyboard input.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True
        elif event.type == pygame.KEYDOWN:
            # update user input when key is pressed
            if event.key == pygame.K_BACKSPACE:
                self.input = self.input[:-1] # delete last digit
            else:
                self.input += event.unicode

    def update(self, player_manager, elapsed_time):
        """
        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
        """
        if self.clicked:
            if self.new_entry and self.enter_button.was_clicked():
                self.update_scores(player_manager)
                self.new_entry = False
            if self.continue_button.was_clicked():
                return GameState.STATS
        self.clicked = False
        return GameState.HALL

    def update_scores(self, player_manager):
        """Write score to file."""
        winner = player_manager.players[player_manager.get_winner()]
        self.scores.append({'name': self.input, 'score': winner.score})
        self.scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)
        for i,score in enumerate(self.scores):
            if score['score'] == winner.score and score['name'] == self.input:
                self.place = i
        with open('scores', 'wb') as file:
            pickle.dump(self.scores, file)

    def draw(self, screen):
        # background color
        screen.fill(Colors.BLACK)
        width, height = screen.get_size()
        if self.new_entry:
            text = Font.number.render('ENTER NAME', True, Colors.GOLD)
            rect = text.get_rect(center=(width/2, height/4))
            screen.blit(text,rect)
            self.enter_button.draw(screen, (width*1/2, height*3/4))
            text = Font.number.render(self.input, True, Colors.WHITE)
            rect = text.get_rect(center=(width/2, height/2))
            screen.blit(text,rect)
        else:
            text = Font.number.render('HIGH SCORES', True, Colors.GOLD)
            rect = text.get_rect(center=(width/2, height/8))
            screen.blit(text,rect)
            self.continue_button.draw(screen, (width*1/2, height*3.5/4))
            # display top 10 scores
            top = min(10, len(self.scores))
            for i in range(top):
                color = Colors.WHITE
                if i == self.place:
                    color = Colors.GOLD
                text = Font.category.render(str(i+1) + '. ' + self.scores[i]['name'], True, color)
                rect = text.get_rect(midleft=(width/2 - 100, height/4 + (i+1)*30))
                screen.blit(text,rect)
                text = Font.category.render( '$' + str(self.scores[i]['score']), True, color)
                rect = text.get_rect(midleft=(width/2 + 100, height/4 + (i+1)*30))
                screen.blit(text,rect)