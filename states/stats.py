"""
Daily Box Scores
"""
from states.state import State
from util.constants import Colors, GameState
from util.util import Button, Font

class Stats(State):
    """Class for displaying game stats at end of game."""
    def __init__(self):
        super().__init__()
        self.continue_button = Button('Return')
        self.stats = []
        self.triple_stumpers = 0

    def startup(self, store, player_manager):
        "Retrieve player stats."
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
            daily_double_str = str(len(player.stats.daily_doubles))
            daily_double_str += ' ' + ', '.join(player.stats.daily_doubles)
            player_stats = [player.number+1, attempts, buzzer, buz_pct,
                str(player.stats.correct) + '/' + str(not_correct),
                correct_pct, daily_double_str, '$' + str(player.score)]
            rendered_text = []
            for stat in player_stats:
                rendered_text.append(Font.category.render( str(stat),  True, Colors.WHITE))
            self.stats.append(rendered_text)
        self.store = store
        self.triple_stumpers = player_manager.triple_stumpers

    def draw(self, screen):
        """Draw player stats grid."""
        screen.fill(Colors.BLACK)
        width, height = screen.get_size()
        text = Font.number.render('GAME TOTALS', True, Colors.GOLD)
        rect = text.get_rect(center=(width/2, 100))
        screen.blit(text,rect)
        self.continue_button.draw(screen, (width*1/2, height*3.5/4))
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

        text = Font.category.render('Triple stumpers: '+str(self.triple_stumpers),True,Colors.WHITE)
        rect = text.get_rect(center=(width/2, len(self.stats)*50 + 300))
        screen.blit(text,rect)

    def update(self, player_manager, elapsed_time):
        """
        Waits for continue button to be clicked.
        Args:
            player_manager (PlayerManager): Reference to manager that keeps track of players
            elapsed_time (int): Milliseconds that have passed since update() was last called

        Returns: TITLE game state when continue is clicked, otherwise continues returning STATS.
        """
        if self.clicked:
            if self.continue_button.was_clicked():
                return GameState.TITLE
        self.clicked = False
        return GameState.STATS
