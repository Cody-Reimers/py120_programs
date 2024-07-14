
import random as r
import sys
import os

sys.path.insert(0, os.getcwd() + "/../resources")

import data_validation as dv

###############################################################################

TTT_CORNERS = {1, 3, 7, 9}
TTT_MIDDLES = {5}

TTT_ROWS = {
    1: (1, 2, 3),
    2: (4, 5, 6),
    3: (7, 8, 9),
}
TTT_COLUMNS = {
    1: (1, 4, 7),
    2: (2, 5, 8),
    3: (3, 6, 9),
}
TTT_DIAGONALS = {
    1: (1, 5, 9),
    2: (3, 5, 7),
}
TTT_LINES = (TTT_ROWS, TTT_COLUMNS, TTT_DIAGONALS)

TTT_MARKS = {"Knots": "O", "Crosses": "X"}
TTT_NULL_MARK = " "

TTT_BOARD_SIZE = 3
TTT_NUM_SQUARES = 9

QUIT = ("q", "quit", "end")

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////////////////////////////////////////////////

class GameLoopEndError(Exception):

    pass

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////////////////////////////////////////////////

def print_program(message, end="\n"):
    print(f"~~~~~~| {message}", end=end)

def print_error(message):
    print(f"ERROR: {message}")

def print_waiting():
    print_program("(INPUT ANYTHING TO CONTINUE) ", '')
    input()
    print_program("")

def get_user_input():
    user_value = input("===> ").strip()

    try:
        if user_value.casefold() in QUIT:
            raise GameLoopEndError("Quitting game loop...")
    except GameLoopEndError as error:
        print_program(error)
        raise GameLoopEndError() from error

    return user_value

def terminal_join(items, seperater=",", terminal_seperater="or"):
    items = [ str(item) for item in items ]

    if len(items) > 2:
        joined_items = f"{seperater} ".join(items[:-1])
        joined_items += f"{seperater} {terminal_seperater} {items[-1]}"
    else:
        joined_items = f" {terminal_seperater} ".join(items)

    return joined_items

def list_of_reprs(collection):
    return [ repr(item) for item in collection ]

def clear_display():
    os.system("cls" if os.name == "nt" else "clear")

###############################################################################

class TTTSquare:

    #~~~~INITIALIZATION~~~~#

    def __init__(self, mark=TTT_NULL_MARK):
        self.mark = mark

    #~~~~GETTER METHODS~~~~#

    @property
    def mark(self):
        return self._mark

    @property
    def is_empty(self):
        return self.mark == TTT_NULL_MARK

    #~~~~SETTER METHODS~~~~#

    @mark.setter
    def mark(self, mark):
        ref = "Square Mark"
        valid_marks = (TTT_NULL_MARK,) + tuple(TTT_MARKS.values())

        dv.error_not_string(mark)
        if mark not in valid_marks:
            raise ValueError(f"{repr(ref)} must be a valid value: " +
                                    terminal_join(list_of_reprs(valid_marks)))

        self._mark = mark

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////////////////////////////////////////////////

class TTTBoard:

    DEFAULT_STATE = TTT_NULL_MARK * 9

    #~~~~INITIALIZATION~~~~#

    def __init__(self):
        self.reset()

    #~~~~GETTER METHODS~~~~#

    @property
    def squares(self):
        return self._squares

    @property
    def empty_squares(self):
        return [ num
             for num in self.squares.keys()
              if self.square_is_empty(num) ]

    def square_mark(self, key):
        return self.squares[key].mark

    def square_alias(self, key):
        mark = self.squares[key].mark
        value = mark if mark != TTT_NULL_MARK else key

        return f"\033[1;36m{value}\x1b[0m"

    def square_is_empty(self, key):
        return self.squares[key].is_empty

    def line_is_empty(self, line_type, line_number):
        identifiers = line_type[line_number]

        return all([ self.square_is_empty(identifier)
                 for identifier in identifiers ])

    def square_is_filled(self, key):
        return self.square_is_empty(key) is False

    def line_is_full(self, line_type, line_number):
        identifiers = line_type[line_number]

        return all([ self.square_is_filled(identifier)
                 for identifier in identifiers ])

    def is_full(self):
        return len(self.empty_squares) == 0

    def line_is_victorious(self, line_type, line_number):
        identifiers = line_type[line_number]
        mark1, mark2, mark3 = [ self.square_mark(identifier)
                            for identifier in identifiers ]

        return ((TTT_NULL_MARK not in (mark1, mark2, mark3))
            and (mark1 == mark2 == mark3))

    def find_block_or_win(self, line_type, line_number):
        if (self.line_is_empty(line_type, line_number)
         or self.line_is_full(line_type, line_number)):
            return False

        identifiers = line_type[line_number]
        mark1, mark2, mark3 = [ self.square_mark(identifier)
                            for identifier in identifiers ]

        if (mark1 == mark2 and mark1 != TTT_NULL_MARK):
            return identifiers[-1]
        if (mark2 == mark3 and mark2 != TTT_NULL_MARK):
            return identifiers[0]
        if (mark3 == mark1 and mark3 != TTT_NULL_MARK):
            return identifiers[1]

        return False

    #~~~~REPRESENTATION~~~~#

    def __str__(self):
        header = ""
        blank_line = "|".join([ ' ' * 5 for _ in range(TTT_BOARD_SIZE) ])
        horizontal_line = "+".join([ '-' * 5 for _ in range(TTT_BOARD_SIZE) ])
        footer = header

        key_sequences = TTT_ROWS.values()
        key_line1, key_line2, key_line3 = [
            "  " + "  |  ".join([ self.square_alias(key) for key in sequence ])
                                        for sequence in key_sequences ]

        return "\n~~~~~~| ".join([
            header,
            blank_line,
            key_line1,
            blank_line,
            horizontal_line,
            blank_line,
            key_line2,
            blank_line,
            horizontal_line,
            blank_line,
            key_line3,
            blank_line,
            footer,
        ])

    def override(self):
        return [ self.square_mark(key + 1) for key in range(TTT_NUM_SQUARES) ]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.override()})"

    #~~~~SETTER METHODS~~~~#

    def update_square(self, key, mark):
        self.squares[key].mark = mark

    def reset(self):
        self._squares = { num + 1: TTTSquare(self.__class__.DEFAULT_STATE[num])
                      for num in range(TTT_NUM_SQUARES) }

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////////////////////////////////////////////////

class TTTPlayer:

    #~~~~INITIALIZATION~~~~#

    def __init__(self, name, mark=TTT_NULL_MARK, is_computer=False):
        self.name = name
        self._mark = mark
        self.is_computer = is_computer

    #~~~~GETTER METHODS~~~~#

    @property
    def name(self):
        return self._name

    @property
    def mark(self):
        return self._mark

    @property
    def is_computer(self):
        return self._is_computer

    #~~~~SETTER METHODS~~~~#

    @name.setter
    def name(self, name):
        ref = "Player Name"

        dv.error_not_string(name, ref)

        self._name = name

    @mark.setter
    def mark(self, mark):
        ref = "Player Mark"
        marks = TTT_MARKS.values()

        dv.error_not_string(mark, ref)
        if mark not in marks:
            raise ValueError(f"{repr(ref)} must be one of " +
                                        terminal_join(list_of_reprs(marks)))

        self._mark = mark

    @is_computer.setter
    def is_computer(self, is_computer):
        ref = "Computer Player Toggle"
        booleans = (True, False)

        if is_computer not in booleans:
            raise ValueError(f"{repr(ref)} must be " +
                                        terminal_join(list_of_reprs(booleans)))

        self._is_computer = is_computer

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////////////////////////////////////////////////

class TTTGame:

    #~~~~AI DECISION MAKING~~~~#

    def _ai_basic_move(self):
        empty_squares = self.board.empty_squares

        empty_middles = TTT_MIDDLES.intersection(empty_squares)
        empty_corners = TTT_CORNERS.intersection(empty_squares)

        if dv.is_empty_set(empty_middles) is False:
            return r.choice(tuple(empty_middles))
        if dv.is_empty_set(empty_corners) is False:
            return r.choice(tuple(empty_corners))

        return r.choice(empty_squares)

    def _ai_find_winning_or_blocking_move(self):
        for line_type in TTT_LINES:
            for line_number in line_type:
                attempt = self.board.find_block_or_win(line_type, line_number)

                if attempt is not False:
                    return attempt

        return False

    #~~~~INITIALIZATION~~~~#

    AI_ALIASES = ("ai", "comp", "computer")

    def __init__(self):
        self._board = TTTBoard()
        self._player1 = TTTPlayer("Player 1")
        self._player2 = TTTPlayer("Player 2")
        self._turn = 1

        print_program("The first thing to do is create the " +
                      "players for the game.")
        while self._player1.mark == TTT_NULL_MARK:
            try:
                self._assign_player(self._player1)
            except (TypeError, ValueError) as error:
                print_error(error)
                self._player1 = TTTPlayer("Player 1")
        while self._player2.mark == TTT_NULL_MARK:
            try:
                self._assign_player(self._player2)
            except (TypeError, ValueError) as error:
                print_error(error)
                self._player2 = TTTPlayer("Player 2")

    def _prompt_get_player_name(self, player):
        print_program(f"You need to provide the name for {player.name}, if " +
                       "you or another human is going to play them;")
        print_program("otherwise, enter one of the following to create a " +
                      "computer Player: " +
                      terminal_join(list_of_reprs(self.__class__.AI_ALIASES)))

    def _assign_player_name(self, player):
        self._prompt_get_player_name(player)
        self._prompt_quit()

        player.name = get_user_input()

    def _prompt_get_player_mark(self, player):
        print_program(f"You also need to choose the mark that {player.name} " +
                       "will use.")
        print_program("Player 2 will automatically use the other mark. The " +
                      "allowed marks are: " +
                      terminal_join(list_of_reprs(TTT_MARKS.values())))

    def _assign_player_mark(self, player):
        if player is self._player2:
            player.mark = [ mark
                        for mark in TTT_MARKS.values()
                         if mark != self._player1.mark ][0]
            return

        self._prompt_get_player_mark(player)
        self._prompt_quit()

        player.mark = get_user_input()

    def _assign_player(self, player):
        self._assign_player_name(player)
        self._assign_player_mark(player)
        player.is_computer = (player.name.casefold()
                           in self.__class__.AI_ALIASES)

    #~~~~FINDING VICTORY~~~~#

    def _is_there_a_victor(self):
        for line_type in TTT_LINES:
            for line_number in line_type:
                attempt = self.board.line_is_victorious(line_type, line_number)

                if attempt is True:
                    return attempt

        return False

    #~~~~GETTER METHODS~~~~#

    @property
    def board(self):
        return self._board

    @property
    def turn(self):
        return self._turn

    def current_player(self):
        return self._player1 if dv.is_odd(self.turn) else self._player2

    def off_turn_player(self):
        return self._player1 if dv.is_even(self.turn) else self._player2

    #~~~~MAKING A MOVE~~~~#

    def _ai_move(self):
        print_program(f"{self.current_player().name} making their move...")
        print_waiting()

        attempt = self._ai_find_winning_or_blocking_move()

        if attempt is not False:
            return attempt

        return self._ai_basic_move()

    def _prompt_human_move(self):
        print_program("It's your turn to mark the board, " +
                     f"{self.current_player().name}!")
        print_program("Available places to mark are: " +
                        terminal_join(list_of_reprs(self.board.empty_squares)))

    def _human_move(self):
        ref = f"{self.current_player().name} Move"
        squares = self.board.empty_squares

        while True:
            self._prompt_human_move()
            self._prompt_quit()

            try:
                attempt = dv.try_to_int(get_user_input())
                dv.error_not_int(attempt, ref)
                if attempt not in squares:
                    raise ValueError(f"{repr(ref)} must be one of " +
                                        terminal_join(list_of_reprs(squares)))
            except (TypeError, ValueError) as error:
                print_error(error)
            else:
                return attempt

    def _get_player_move(self):
        return (self._ai_move()
             if self.current_player().is_computer
           else self._human_move())

    #~~~~PROMPTS~~~~#

    def _prompt_quit(self):
        print_program("Or you can quit by inputting one of the following: " +
                      terminal_join(list_of_reprs(QUIT)))

    #~~~~PLAYING THE GAME~~~~#

    def _display_introduction(self):
        print_program("Welcome to the Object-Oriented Tic-Tac-Toe game!")
        print_waiting()

    def _display_board_state(self, time_frame):
        if self.turn != 1:
            clear_display()
        print_program(f"Here's the {time_frame} board state:")
        print_program(self.board)
        print_waiting()

    def _display_endgame(self, where_final_move_at):
        if self.board.is_full():
            print_program("You both ran out of valid moves; the game is tied!")
            return

        print_program(f"{self.current_player().name} won! They played the " +
                      f"final move at square {where_final_move_at}!")

    def _display_conclusion(self):
        print_program("Thanks for playing the Object-Oriented " +
                      "Tic-Tac-Toe game!")
        print_waiting()

    def play_one_game(self):
        clear_display()
        self._display_introduction()
        self.board.reset()
        move, victory = None, False

        while victory is False:
            if self.current_player().is_computer is False:
                self._display_board_state("current")

            move = self._get_player_move()
            self.board.update_square(move, self.current_player().mark)

            if self.current_player().is_computer is False:
                self._display_board_state("new")

            victory = self._is_there_a_victor() or self.board.is_full()
            self.turn += 1 if victory is False else 0

        self._display_board_state("final")
        self._display_endgame(move)

    def play_again(self):
        continuing_answers = ("y", "yes", "continue", "again")
        choice = None
        ref = "Play Again Choice"

        while choice not in continuing_answers:
            print_program("Do you want to play another round of this game?")
            self._prompt_quit()

            try:
                choice = get_user_input()
                if choice not in continuing_answers:
                    raise ValueError(f"{repr(ref)} must be one of " +
                            terminal_join(list_of_reprs(continuing_answers)))
            except ValueError as error:
                print_error(error)

    def play(self):
        while True:
            self.play_one_game()

            try:
                self.play_again()
            except GameLoopEndError:
                break

        self._display_conclusion()

    #~~~~SETTER METHODS~~~~#

    @turn.setter
    def turn(self, turn):
        ref = "Tic-Tac-Toe Game Turn"
        valid_turn_numbers = range(1, TTT_NUM_SQUARES + 1)

        dv.error_not_int(turn)
        if turn not in valid_turn_numbers:
            raise ValueError(f"{repr(ref)} must be one of " +
                            terminal_join(list_of_reprs(valid_turn_numbers)))

        self._turn = turn

###############################################################################

try:
    game = TTTGame()
    game.play()
except GameLoopEndError:
    pass
finally:
    print_program("See you next time!")
