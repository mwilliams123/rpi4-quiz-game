"""
Manager that keeps track of players and provides an easy interface
for other classes to access/update player score and status.
"""
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
    """
    def __init__(self):
        self.players = [Player(19, 6, 0, self), Player(16, 21, 1, self), Player(12, 17, 2, self)]
        try:
            self.stoplight = gpiozero.RGBLED(red=18, blue=24, green=23)
        except gpiozero.exc.PinPWMUnsupported:
            class MockRGB():
                """Mock hardware when not run on RPi."""
            self.stoplight = MockRGB()
        self.stoplight.color = (0,0,0)
        self.rung_in = None
        self.control = 0

    def green_light(self):
        """Turns on light to let players know they can ring in.

        Called immediately after a question is read."""
        self.stoplight.color = (0, 1, 0)
        self.rung_in = None
        for player in self.players:
            player.eligible = True
            player.timer = 5000

    def reset(self):
        """Prevents all players from ringing in, resets lights.

        Called after question is answered or timer has experied."""
        self.stoplight.color = (0,0,0)
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
        if self.players[self.rung_in].timer <= 0:
            return True

        # count down timer of player that rung in
        self.players[self.rung_in].update_timer(elapsed_time)
        return False

    def ring_in(self, player):
        """Records first player to ring in and locks out other players."""
        self.rung_in = player
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

    def update_control(self):
        """Gives control to the player with the lowest score at start of second round."""
        lowest = float('inf')
        for player in self.players:
            if player.score < lowest:
                lowest = player.score
                self.control = player.number
