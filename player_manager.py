"""
Manager that keeps track of players and provides an easy interface
for other classes to access/update player score and status.
"""
from types import SimpleNamespace
import gpiozero
from player import Player

class PlayerManager():
    """
    Class for keeping track of players and hardware.

    Attributes:
        players (list of Players): a Player object for each player in the game
        stoplight (RGBLED): a multicolor light that comes on when players can ring in
            color is specified as (Red, Green, Blue) integer values between 0 and 1.
        ring_in (int): The id of the player who rung in
        control (int): The id of the player who has control of the board (picks the next question)
        timer (int): Time in milliseconds left to answer question
    """
    def __init__(self):
        self.players = [Player(19, 6, 0, self), Player(16, 21, 1, self), Player(12, 17, 2, self)]
        try:
            self.stoplight = gpiozero.RGBLED(red=18, blue=24, green=23)
        except gpiozero.exc.PinPWMUnsupported:
            self.stoplight = SimpleNamespace() # create mock hardware
        self.stoplight.color = (0,0,0)
        self.rung_in = None
        self.control = 0
        self.timer = 5000

    def green_light(self):
        """Turns on light to let players know they can ring in.

        Called immediately after a question is read."""
        self.stoplight.color = (0, 1, 0)
        self.rung_in = None
        for player in self.players:
            player.eligible = True

    def reset(self):
        """Prevents all players from ringing in, resets lights.

        Called after question is answered or timer has experied."""
        self.stoplight.color = (0,0,0)
        self.timer = 5000
        for player in self.players:
            player.eligible = False
            player.led.off()

    def poll(self, elapsed_time):
        """Counts down player timer and checks to see if time has expired.

        Args:
            elapsed_time (int): Milliseconds that have passed since poll() was last called

        Returns:
            boolean: True if player timer has expired
        """
        if self.timer <= 0:
            return True

        # count down timer of player that rung in
        self.timer -= elapsed_time
        return False

    def ring_in(self, player_id):
        """Records first player to ring in and locks out other players.

        Args:
            player_id (int): Id number of player who rung in
        """
        self.rung_in = player_id
        for player in self.players:
            player.eligible = False

    def update(self, correct, value):
        """Adds clue's dollar amount to player's score if answer is correct,
        otherwise decrements their score. Gives them control of board if correct.

        Args:
            correct (boolean): Whether the question was answered correctly
            value (int): Dollar amount of question
        """
        # update player score for player who rung in
        self.players[self.rung_in].answer_question(correct, value)
        # give control to player with correct answer
        if correct:
            self.control = self.rung_in
        self.rung_in = None

    def update_control(self):
        """Gives control to the player with the lowest score at start of second round."""
        lowest = float('inf')
        for player in self.players:
            if player.score < lowest:
                lowest = player.score
                self.control = player.number
