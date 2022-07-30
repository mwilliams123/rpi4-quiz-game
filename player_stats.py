class PlayerStats:
    def __init__(self) -> None:
        self.attempts = 0
        self.questions_answered = 0
        self.correct = 0
        self.daily_doubles = []
        self.buzzers = 0
        self.active_round = False

    def record_buzzer(self):
        if self.active_round:
            self.buzzers += 1

    def record_clue(self):
        self.active_round = True

    def record_questions_stats(self):
        if self.buzzers > 0:
            self.attempts += 1
            self.buzzers = 0
        self.active_round = False

    def record_answer(self):
        self.questions_answered += 1

    def record_correct(self):
        self.correct += 1

    def record_daily_double(self, amt, correct):
        if correct:
            self.daily_doubles.append('$' + str(amt))
        else:
            self.daily_doubles.append('-$' + str(amt))

    def print_stats(self):
        print('Questions attempted: ' + str(self.attempts))
        print('Questions answered: ' + str(self.questions_answered))
        print('Questions correct: ' + str(self.correct))
        print('Daily doubles answered: ' + str(self.daily_doubles))
        print('Daily doubles correct: ' + str(self.daily_doubles_correct))
        print('\n')
