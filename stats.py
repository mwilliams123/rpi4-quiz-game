# Daily Box Scores
import pygame
from util import Button, display_text, Font
from state import State
from constants import Colors, GameState

# player.attempts
# player.buzzers
# player.correct
# player.not_correct
# player.streak (for LS)
# player.dd
# player.dd1 (in double jeopardy)
# player.dd2
# player.final_score

# Jeopardy Round
# ATT, BUZ, BUZ %, COR/NC, CORRECT %, LS, DD, EOR SCORE

# Double Jeopardy
# ATT, BUZ, BUZ %, COR/NC, CORRECT %, LS, DD #1, DD #2, EOR SCORE

# Final Jeopardy
# FJ WAGER, FINAL SCORE

# Game Totals
# ATT, BUZ, BUZ%, COR/NC, CORRECT %, DD(COR/NC), FINAL SCORE

# Cumulative Totals: TOTAL WINNINGS, GAMES WON, BUZ%, COR/NC
# CORRECT%, DD(COR/NC), DD%, FJ(COR/NC) FJ%

# return to main menu after displa

class Stats(State): 

    def __init__(self):
        super().__init__()
        self.name = GameState.STATS
        self.continue_button = Button('Return')
        self.clicked = False
        self.stats = []
        self.triple_stumpers = 0

    def startup(self, store, player_manager):
        # players data
        for player in player_manager.players:
            buzzer = player.stats.questions_answered
            attempts = player.stats.attempts
            if attempts == 0:
                buz_pct = 'N/A'
                
            else:
                buz_pct = str(int(100*buzzer/attempts)) + '%'
            if buzzer == 0:
                correct_pct = 'N/A'
            else:
                correct_pct = str(int(100*player.stats.correct/buzzer)) + '%'
            not_correct = buzzer - player.stats.correct
            daily_double_str = str(len(player.stats.daily_doubles)) + ' ' + ', '.join(player.stats.daily_doubles)
            player_stats = [player.number+1, attempts, buzzer, buz_pct, str(player.stats.correct) + '/' + str(not_correct),
                correct_pct, daily_double_str, '$' + str(player.score)]
            rendered_text = []
            for stat in player_stats:
                rendered_text.append(Font.category.render( str(stat),  True, Colors.WHITE))
            self.stats.append(rendered_text)
        self.store = store
        self.triple_stumpers = player_manager.triple_stumpers
       
# Draw for scores
    def draw(self, screen):
    
    # background color
        screen.fill(Colors.BLACK)
    # x, y, width, height   (coordinates of top left corner)
        width, height = screen.get_size()
    # draw title; Jeopardy! Daily Box Score, date
        text = Font.number.render('GAME TOTALS', True, Colors.GOLD)
        rect = text.get_rect(center=(width/2, 100))
        screen.blit(text,rect)
        self.continue_button.draw(screen, (width*1/2, height*3.5/4))
        
    # Draw BLUE background in rectangle, for column headings
       # pygame.draw.rect(screen, Colors.BLUE, pygame.Rect(30, 30, width, 20))
       # pygame.display.blit()
    # Column Headings: Player, ATT, BUZ, BUZ %
        stats = ['PLAYER', 'ATT' , 'BUZ' , 'BUZ%' ,  'COR/INC', 'CORRECT %' ,'DD' , 'FINAL SCORE']
        for i, stat in enumerate(stats):
            text = Font.category.render(stat, True, Colors.WHITE)
            box_width = (width - 50) / len(stats)
            rect = text.get_rect(midleft=(50 + box_width*i, 200))
            screen.blit(text,rect)
        
            for j, player_stats in enumerate(self.stats):
                text = player_stats[i]
                rect = text.get_rect(midleft=(50 + box_width*i, 250 + j*50))
                screen.blit(text,rect)
    
        text = Font.category.render('Triple stumpers: ' + str(self.triple_stumpers), True, Colors.WHITE)
        rect = text.get_rect(center=(width/2, len(self.stats)*50 + 300))
        screen.blit(text,rect)
    # KEY (inside gray rectangle): 
    # ATT: Attempts to Buzz in; 
    # BUZ - Number of times contesntant buzzed in; 
    # BUZ% Pct. Indiv Contestant buzzed in vs. attempts  (BUZ/ATT)
    # COR/INC: How many correct/incorrect responses
    # CORRECT %: Pct of correct responses (COR/(COR+INC))
    # DD(COR/INC): Daily Double
    # FINAL SCORE

        

    #event handler: check to see if user clicked mouse
    def handle_event(self, event):
        """
        Sets flag when left mouse is clicked. Captures user keyboard input.

        Args:
            event (Event): Pygame Event such as a mouse click or keyboard press.
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = True
            
    #update: if user chooses continue, return to play screen
    def update(self, player_manager, elapsed_time):
        """
        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns:
        """
        if self.clicked:
            if self.continue_button.was_clicked():
                return GameState.TITLE
        self.clicked = False
        return GameState.STATS