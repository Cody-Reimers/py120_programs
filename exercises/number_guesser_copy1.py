
import random as r
import os
import sys

sys.path.insert(0, os.getcwd() + "/..")
# Allows importing of data_validation

from resources import data_validation as dv

###############################################################################

class Player:
    def __init__(self):
        self._print_game_message("Who is playing?")
        self._name = input("===> ")

    @property
    def name(self):
        return self._name

    def make_guess(self):
        guess = ""
        valid = False

        while not valid:
            guess = input("===> ")
            guess = dv.try_to_int(guess)

            if dv.is_int(guess) is False:
                self._print_game_message("Invalid choice, must provide " +
                                   "an integer value.")
            elif 100 < guess or 1 > guess:
                self._print_game_message("Invalid choice, must choose a " +
                              "value between 1 and 100.")
            else:
                valid = True

        return guess

#~~~~STATIC METHODS~~~~#

    @staticmethod
    def _print_game_message(message):
        print(f"~~~~~~| {message}")




class GuessingGame:
#~~~~CLASS CONSTANTS~~~~#

    SECRET_RANGE = range(1, 100 + 1)
    MAX_GUESSES = 7

#~~~~DUNDER METHODS~~~~#

    def __init__(self):
        self._player = Player()
        self._target = None
        self._guesses_remaining = None
        self._victorious = False
        self._current_guess = None

#~~~~GETTER METHODS~~~~#

    @property
    def player(self):
        return self._player

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
        self._target = r.choice(self.SECRET_RANGE)
        self._guesses_remaining = self.MAX_GUESSES
        self._victorious = False
        self._current_guess = None

#~~~~GETTING A GUESS~~~~#

    def _prompt_user(self):
        guesses = self.guesses_remaining
        player_name = self.player.name

        if guesses == 1:
            self._print_game_message(f"{player_name}, you have " +
                                     f"{guesses} guess remaining.")
        else:
            self._print_game_message(f"{player_name}, you have " +
                                     f"{guesses} guesses remaining.")

        self._print_game_message(f"Enter a number between 1 and 100.")

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
        self._current_guess = self._player.make_guess()
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

###############################################################################

game = GuessingGame()
game.play()
game.play()
game.play()
