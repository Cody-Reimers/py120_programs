
import random as r
import os
import sys

sys.path.insert(0, os.getcwd() + "/..")

from resources import data_validation as dv

###############################################################################

CARD_RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace")
CARD_SUITS = ("Diamonds", "Clubs", "Hearts", "Spades")

###############################################################################

class Deck:
#~~~~CLASS VALUES~~~~#

    NUMBER_OF_CARDS = len(CARD_RANKS) * len(CARD_SUITS)
    _default_deck = ()

#~~~~DUNDER METHODS~~~~#

    def __init__(self):
        if bool(self._default_deck) is False:
            self._initialize_default()

        self._deck = []
        self._reshuffle_deck()

#~~~~USING A DECK~~~~#

    def _reshuffle_deck(self):
        self._deck = r.sample(self._default_deck, self.NUMBER_OF_CARDS)

    def draw(self):
        card = self._deck.pop()

        if len(self._deck) == 0:
            self._reshuffle_deck()

        return card

#~~~~CLASS METHODS~~~~#

    @classmethod
    def _initialize_default(cls):
        cls._default_deck = tuple([ Card(rank, suit) for rank in CARD_RANKS
                                                     for suit in CARD_SUITS ])

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////////////////////////////////////////////////

class Card:
#~~~~CLASS VALUES~~~~#

    NUMBER_OF_SUITS = len(CARD_SUITS)
    _card_values = {}

#~~~~DUNDER METHODS~~~~#

    def __init__(self, rank, suit):
        self._validate_arguments(rank, suit)

        if bool(self._card_values) is False:
            self._initialize_values()

        self._rank = rank
        self._suit = suit

    def __str__(self):
        rank, suit = self.rank, self.suit
        return f"{rank} of {suit}"

    def __eq__(self, other):
        return self._comparitor(other, "==")

    def __ne__(self, other):
        return self._comparitor(other, "!=")

    def __lt__(self, other):
        return self._comparitor(other, "<")

    def __gt__(self, other):
        return self._comparitor(other, ">")

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

#~~~~GETTER METHODS~~~~#

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit

#~~~~DETERMINING CARD VALUE~~~~#

    def _comparitor(self, other, operator):
        if dv.other_is_same_type(type(self), other) is False:
            return NotImplemented

        value1 = self._card_values[str(self)]
        value2 = self._card_values[str(other)]

        match operator:
            case "==":
                return value1 == value2
            case "!=":
                return value1 != value2
            case "<":
                return value1 < value2
            case ">":
                return value1 > value2

#~~~~INSTANCE UTILITIES~~~~#

    def _validate_arguments(self, rank, suit):
        dv.error_not_int_or_string(rank, "Rank")
        dv.error_not_string(suit, "Suit")

        valid_ranks = CARD_RANKS
        valid_suits = CARD_SUITS

        if dv.try_to_int(rank) not in valid_ranks:
            raise ValueError("Rank argument must be a valid card rank: " +
                            ", ".join(valid_ranks))
        if suit.title() not in valid_suits:
            raise ValueError("Suit argument must be a valid card suit: " +
                            ", ".join(valid_suits))

#~~~~CLASS METHODS~~~~#

    @classmethod
    def _initialize_values(cls):
        cls._card_values = {
            f"{rank} of {suit}": 1 + i2 + (i1 * cls.NUMBER_OF_SUITS)
            for i1, rank in enumerate(CARD_RANKS)
            for i2, suit in enumerate(CARD_SUITS)
        }

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////////////////////////////////////////////////

class PokerHand:
#~~~~CLASS VALUES~~~~#

    CARDS_IN_A_HAND = 5

#~~~~DUNDER METHODS~~~~#

    def __init__(self, deck):
        self.hand = []

        for _ in range(self.CARDS_IN_A_HAND):
            self.hand.append(deck.draw())

#~~~~USING A HAND~~~~#

    def print(self):
       for card in self.hand:
           print(card)

    def evaluate(self):
        evaluation = "_is_high_card"
        ranks, suits = {}, {}

        for card in self.hand:
            rank, suit = card.rank, card.suit
            ranks[rank] = ranks.setdefault(rank, 0) + 1
            suits[suit] = suits.setdefault(suit, 0) + 1

        for method in self._evaluation_methods_list():
            if method(ranks, suits) is True:
                evaluation = method.__name__
                break

        return evaluation.replace("_", " ")[4:].capitalize()
# Ex: processes "_is_high_card" into "High card"

#~~~~EVALUATION METHODS~~~~#

    def _evaluation_methods_list(self):
        return (
            self._is_royal_flush, self._is_straight_flush,
            self._is_four_of_a_kind, self._is_full_house, self._is_flush,
            self._is_straight, self._is_three_of_a_kind,
            self._is_two_pair, self._is_pair
        )

    def _is_royal_flush(self, ranks, suits):
        if (self._is_straight(ranks, suits)
        and self._is_flush(ranks, suits)
        and all([ rank in set(CARD_RANKS[-5:]) for rank in ranks ])):
        # Ensures cards are all royals, 10, and Ace
            return True

        return False

    def _is_straight_flush(self, ranks, suits):
        return (self._is_flush(ranks, suits)
            and self._is_straight(ranks, suits))

    def _is_four_of_a_kind(self, ranks, suits):
        return max(ranks.values()) > 3

    def _is_full_house(self, ranks, suits):
        return (self._is_two_pair(ranks, suits)
            and self._is_three_of_a_kind(ranks, suits))

    def _is_flush(self, ranks, suits):
        return len(suits) == 1

    def _is_straight(self, ranks, suits):
        if len(ranks) < self.CARDS_IN_A_HAND:
            return False

        indices = []
        for rank in ranks:
            indices.append(CARD_RANKS.index(rank))

        if (max(indices) - min(indices) == 4
        or all([ rank in set(CARD_RANKS[:4] + (CARD_RANKS[-1],))
             for rank in ranks])):
# Creates an exception that allows low-Ace straights to be valid
            return True

        return False

    def _is_three_of_a_kind(self, ranks, suits):
        return max(ranks.values()) > 2

    def _is_two_pair(self, ranks, suits):
        goal = 2
        current = 0

        for value in ranks.values():
            if value > 1:
                current += 1

        return current == goal

    def _is_pair(self, ranks, suits):
        return max(ranks.values()) > 1

###############################################################################

cards = [Card(2, 'Hearts'),
         Card(10, 'Diamonds'),
         Card('Ace', 'Clubs')]
print(min(cards) == Card(2, 'Hearts'))             # True
print(max(cards) == Card('Ace', 'Clubs'))          # True
print(str(min(cards)) == "2 of Hearts")            # True
print(str(max(cards)) == "Ace of Clubs")           # True

cards = [Card(5, 'Hearts')]
print(min(cards) == Card(5, 'Hearts'))             # True
print(max(cards) == Card(5, 'Hearts'))             # True
print(str(Card(5, 'Hearts')) == "5 of Hearts")     # True

cards = [Card(4, 'Hearts'),
         Card(4, 'Diamonds'),
         Card(10, 'Clubs')]
print(min(cards).rank == 4)                        # True
print(max(cards) == Card(10, 'Clubs'))             # True
print(str(Card(10, 'Clubs')) == "10 of Clubs")     # True

cards = [Card(7, 'Diamonds'),
         Card('Jack', 'Diamonds'),
         Card('Jack', 'Spades')]
print(min(cards) == Card(7, 'Diamonds'))           # True
print(max(cards).rank == 'Jack')                   # True
print(str(Card(7, 'Diamonds')) == "7 of Diamonds") # True

cards = [Card(8, 'Diamonds'),
         Card(8, 'Clubs'),
         Card(8, 'Spades')]
print(min(cards).rank == 8)                        # True
print(max(cards).rank == 8)                        # True

deck = Deck()
drawn = []
for _ in range(52):
    drawn.append(deck.draw())

count_rank_5 = sum([1 for card in drawn if card.rank == 5])
count_hearts = sum([1 for card in drawn if card.suit == 'Hearts'])

print(count_rank_5 == 4)      # True
print(count_hearts == 13)     # True

drawn2 = []
for _ in range(52):
    drawn2.append(deck.draw())

print(drawn != drawn2)        # True (Almost always).

hand = PokerHand(Deck())
hand.print()
print(hand.evaluate())
print()

# Adding TestDeck class for testing purposes

class TestDeck(Deck):
    def __init__(self, cards):
        self._deck = cards

# All of these tests should return True

hand = PokerHand(
    TestDeck(
        [
            Card("Ace", "Hearts"),
            Card("Queen", "Hearts"),
            Card("King", "Hearts"),
            Card("Jack", "Hearts"),
            Card(10, "Hearts"),
        ]
    )
)
print(hand.evaluate() == "Royal flush")

hand = PokerHand(
    TestDeck(
        [
            Card(8, "Clubs"),
            Card(9, "Clubs"),
            Card("Queen", "Clubs"),
            Card(10, "Clubs"),
            Card("Jack", "Clubs"),
        ]
    )
)
print(hand.evaluate() == "Straight flush")

hand = PokerHand(
    TestDeck(
        [
            Card(3, "Hearts"),
            Card(3, "Clubs"),
            Card(5, "Diamonds"),
            Card(3, "Spades"),
            Card(3, "Diamonds"),
        ]
    )
)
print(hand.evaluate() == "Four of a kind")

hand = PokerHand(
    TestDeck(
        [
            Card(3, "Hearts"),
            Card(3, "Clubs"),
            Card(5, "Diamonds"),
            Card(3, "Spades"),
            Card(5, "Hearts"),
        ]
    )
)
print(hand.evaluate() == "Full house")

hand = PokerHand(
    TestDeck(
        [
            Card(10, "Hearts"),
            Card("Ace", "Hearts"),
            Card(2, "Hearts"),
            Card("King", "Hearts"),
            Card(3, "Hearts"),
        ]
    )
)
print(hand.evaluate() == "Flush")

hand = PokerHand(
    TestDeck(
        [
            Card(8, "Clubs"),
            Card(9, "Diamonds"),
            Card(10, "Clubs"),
            Card(7, "Hearts"),
            Card("Jack", "Clubs"),
        ]
    )
)
print(hand.evaluate() == "Straight")

hand = PokerHand(
    TestDeck(
        [
            Card("Queen", "Clubs"),
            Card("King", "Diamonds"),
            Card(10, "Clubs"),
            Card("Ace", "Hearts"),
            Card("Jack", "Clubs"),
        ]
    )
)
print(hand.evaluate() == "Straight")

hand = PokerHand(
    TestDeck(
        [
            Card(3, "Hearts"),
            Card(3, "Clubs"),
            Card(5, "Diamonds"),
            Card(3, "Spades"),
            Card(6, "Diamonds"),
        ]
    )
)
print(hand.evaluate() == "Three of a kind")

hand = PokerHand(
    TestDeck(
        [
            Card(9, "Hearts"),
            Card(9, "Clubs"),
            Card(5, "Diamonds"),
            Card(8, "Spades"),
            Card(5, "Hearts"),
        ]
    )
)
print(hand.evaluate() == "Two pair")

hand = PokerHand(
    TestDeck(
        [
            Card(2, "Hearts"),
            Card(9, "Clubs"),
            Card(5, "Diamonds"),
            Card(9, "Spades"),
            Card(3, "Diamonds"),
        ]
    )
)
print(hand.evaluate() == "Pair")

hand = PokerHand(
    TestDeck(
        [
            Card(2, "Hearts"),
            Card("King", "Clubs"),
            Card(5, "Diamonds"),
            Card(9, "Spades"),
            Card(3, "Diamonds"),
        ]
    )
)
print(hand.evaluate() == "High card")
