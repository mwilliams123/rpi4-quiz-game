# Daily Box Scores
import pygame
from util import display_text, Font
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
       
# Draw for scores
    def draw(self, screen):
    
    # background color
        screen.fill(Colors.BLACK)
    # x, y, width, height   (coordinates of top left corner)
        width, height = screen.get_size()
    # draw title; Jeopardy! Daily Box Score, date
        text = Font.category.render('GAME TOTALS', True, Colors.GOLD)
        rect = text.get_rect(center=(width/2, height/2))
        screen.blit(text,rect)
        self.continue_button.draw(screen, (width*1/2, height*3.5/4))
        
    # Draw BLUE background in rectangle, for column headings
       # pygame.draw.rect(screen, Colors.BLUE, pygame.Rect(30, 30, width, 20))
       # pygame.display.blit()
    # Column Headings: Player, ATT, BUZ, BUZ %
        text = Font.category.render('PLAYER' + '    ' + 'ATT' + '    ' + 'BUZ' + '    ' + 'BUZ%' + '    ' 
        + '   ' + 'COR/INC' + '    ' + 'CORRECT %' + '    ' + 'DD' + '    ' + 'FINAL SCORE', True, Colors.WHITE)
        rect = text.get_rect(midleft=(width/2 - 100, height/4 + (i+1)*30))
        screen.blit(text,rect)
        
    # players data
        for player in player_manager.players:
            buz_pct = player.buzzer/player.attempts
            correct_pct = player.correct/(player.correct + player.not_correct)
            text = Font.category.render( str(player.num+1) + '    ' + str(player.attempts) + str(player.buzzers) + '    ' +
                str(buz_pct) + '    ' + str(player.correct) + '/' + str(player.not_correct) + '    ' + str(correct_pct) + '   ' +
                str(player.dd) + '   ' + str(player.score), True, Colors.WHITE)
            rect = text.get_rect(midleft=(width/2 + 100, height/4 + (i+1)*30))
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