
import random as r
import math
import os
import sys

sys.path.insert(0, os.getcwd() + "/..")
# Allows importing of data_validation

from resources import data_validation as dv

###############################################################################

class GuessingGame:
#~~~~CLASS CONSTANTS~~~~#

    DEFAULT_MIN = 1
    DEFAULT_MAX = 100
    DEFAULT_RANGE = range(1, 100)
    DEFAULT_MAX_GUESSES = 7

#~~~~CLASS VARIABLES~~~~#

    _secret_min = DEFAULT_MIN
    _secret_max = DEFAULT_MAX
    _secret_range = DEFAULT_RANGE
    _max_guesses = DEFAULT_MAX_GUESSES

#~~~~DUNDER METHODS~~~~#

    def __init__(self, low=None, high=None):
        self._target = None
        self._guesses_remaining = None
        self._victorious = False
        self._current_guess = None

        GuessingGame._check_for_class_updates(low, high)

#~~~~GETTER METHODS~~~~#

    @property
    def target(self):
        return self._target

    @property
    def guesses_remaining(self):
        return self._guesses_remaining

    @property
    def victorious(self):
        return self._victorious

    @property
    def current_guess(self):
        return self._current_guess

#~~~~INITIALIZING A NEW GAME~~~~#

    def _reinitialize(self):
        self._target = r.choice(self.secret_range())
        self._guesses_remaining = self.max_guesses()
        self._victorious = False
        self._current_guess = None

#~~~~GETTING A GUESS~~~~#

    def _prompt_user(self):
        guesses = self.guesses_remaining

        if guesses == 1:
            self._print_game_message(f"You have {guesses} guess remaining.")
        else:
            self._print_game_message(f"You have {guesses} guesses remaining.")

        low, high = self.secret_min(), self.secret_max()
        self._print_game_message(f"Enter a number between {low} and {high}.")

    def _get_guess(self):
        guess = ""
        valid = False

        while not valid:
            guess = input("===> ")
            guess = dv.try_to_int(guess)

            if dv.is_int(guess) is False:
                self._print_game_message("Invalid choice, must provide " +
                                   "an integer value.")
            elif self.secret_max() < guess or self.secret_min() > guess:
                self._print_game_message("Invalid choice, must choose a " +
                              "value between 1 and 100.")
            else:
                valid = True

        self._current_guess = guess

#~~~~REPORTING THE SITUATION~~~~#

    def _report_higher_lower(self):
        high_or_low = "high" if self.current_guess > self.target else "low"
        self._print_game_message(f"Your guess is too {high_or_low}.")

    def _report_win_loss(self):
        if self.victorious:
            self._print_game_message("That's the number!")
            self._print_game_message('')
            self._print_game_message("You won!")
        else:
            self._print_game_message("")
            self._print_game_message("You have no more guesses! You lost!")

#~~~~RUNNING A GAME~~~~#

    def _game_loop(self):
        self._prompt_user()
        self._get_guess()
        self._victorious = self.current_guess == self.target

        self._guesses_remaining -= 1

    def play(self):
        self._reinitialize()

        while self.guesses_remaining > 0:
            self._game_loop()

            if self.victorious:
                break

            self._report_higher_lower()

        self._report_win_loss()

#~~~~STATIC METHODS~~~~#

    @staticmethod
    def _print_game_message(message):
        print(f"~~~~~~| {message}")

#~~~~CLASS METHODS~~~~#

    @classmethod
    def secret_min(cls):
        return cls._secret_min

    @classmethod
    def secret_max(cls):
        return cls._secret_max

    @classmethod
    def secret_range(cls):
        return cls._secret_range

    @classmethod
    def max_guesses(cls):
        return cls._max_guesses

    @classmethod
    def _set_secret_min(cls, new):
        cls._secret_min = new

    @classmethod
    def _set_secret_max(cls, new):
        cls._secret_max = new

    @classmethod
    def _make_secret_range(cls, low, high):
        cls._secret_range = range(low, high + 1)

    @classmethod
    def _set_max_guesses(cls):
        cls._max_guesses = 1 + int(math.log2(cls.secret_max() -
                                             cls.secret_min() + 1))
# "cls.secret_max()" is the highest number in the range
# "cls.secret_min()" is the lowest number in the range

    @classmethod
    def _check_for_class_updates(cls, low, high):
        if low is None and high is None:
            return
        elif None not in (low, high):
            dv.error_not_int(low, "Minimum value")
            dv.error_not_int(high, "Maximum value")

            GuessingGame._set_secret_min(low)
            GuessingGame._set_secret_max(high)
            GuessingGame._make_secret_range(low, high)
            GuessingGame._set_max_guesses()
        else:
            _class = cls.__name__
            raise TypeError(f"Must provide 0 or 2 arguments to {_class}.")

###############################################################################

game = GuessingGame(501, 1500)
game.play()
