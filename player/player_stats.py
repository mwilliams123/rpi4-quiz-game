"""
Module for keeping track of player stats.
"""

class PlayerStats:
    """
    Statistics of player buzzer attempts and questions answered.

     Attributes:
        attempts (int): Number of questions player attempted to ring in on.
        questions_answered (int): Number of questions player succesfully rang in on.
        correct (int): Number of questions answered correctly.
        daily_doubles (list of str): List of wagers made on daily doubles. Wagers
            are negative if question was answered incorrectly.
        buzzers (int): Number of times buzzer was physically pressed on a question.
        active_round (bool): True if and only if players can ring in currently.
    """
    def __init__(self) -> None:
        self.attempts = 0
        self.questions_answered = 0
        self.correct = 0
        self.daily_doubles = []
        self.buzzers = 0
        self.active_round = False

    def record_buzzer(self):
        """Record each time a player physically presses their button."""
        if self.active_round:
            self.buzzers += 1

    def record_clue(self):
        """Players can now ring in."""
        self.active_round = True

    def record_questions_stats(self):
        """Record whether player attempted to ring in."""
        if self.buzzers > 0:
            self.attempts += 1
            self.buzzers = 0
        self.active_round = False

    def record_answer(self):
        """Record when player wins buzzer."""
        self.questions_answered += 1

    def record_correct(self):
        """Record player answered correctly."""
        self.correct += 1

    def record_daily_double(self, amt, correct):
        """Record player answering daily double."""
        if correct:
            self.daily_doubles.append('$' + str(amt))
        else:
            self.daily_doubles.append('-$' + str(amt))

    def print_stats(self):
        """Debug player stats display."""
        print('Questions attempted: ' + str(self.attempts))
        print('Questions answered: ' + str(self.questions_answered))
        print('Questions correct: ' + str(self.correct))
        print('Daily doubles answered: ' + str(self.daily_doubles))
        print('\n')
