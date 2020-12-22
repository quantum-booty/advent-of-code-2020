# With help from Joel Grus. I really suck at doing recursion!
# But I've learned a valueble lesson: recursion in a lot easier to do with
# self.attributes than with return values! Not needing to keep track of what
# returns what is a huge convenience. Also using the appropriate data structure
# can simplify the problem. In this case, since we are popping from left and
# appending to the right, deque would be the natural choice instead of list.

from typing import List, Set, Tuple, Optional, Deque
from collections import deque


class Game:
    def __init__(self, deck1: List[int], deck2: List[int]) -> None:
        self.deck1: Deque[int] = deque(deck1)
        self.deck2: Deque[int] = deque(deck2)
        self.winner: Optional[int] = None

    def play_round(self) -> None:
        # assuming each player can't have the same card.
        card1 = self.deck1.popleft()
        card2 = self.deck2.popleft()
        if card1 > card2:
            # player 1 win round
            self.deck1.extend([card1, card2])
        elif card2 > card1:
            # player 2 win round
            self.deck2.extend([card2, card1])
        else:
            raise RuntimeError("cards were equal")

        if not self.deck1:
            self.winner = 2
        elif not self.deck2:
            self.winner = 1

    def play_until_win(self) -> None:
        while not self.winner:
            self.play_round()

    def winner_score(self) -> int:
        if not self.winner:
            raise RuntimeError("Game is not over")
        winner_deck = self.deck1 or self.deck2
        return sum(card_value * order
                   for card_value, order in zip(winner_deck, range(len(winner_deck), 0, -1)))


class RecursiveGame(Game):
    def __init__(self, deck1: List[int], deck2: List[int]) -> None:
        super().__init__(deck1, deck2)
        self.seen: Set = set()
        self.winner: Optional[int] = None

    def signature(self) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        return (tuple(self.deck1), tuple(self.deck2))

    def play_round(self) -> None:
        sig = self.signature()
        if sig in self.seen:
            self.winner = 1
            return
        else:
            self.seen.add(sig)

        card1 = self.deck1.popleft()
        card2 = self.deck2.popleft()

        if card1 <= len(self.deck1) and card2 <= len(self.deck2):
            # winner is determined by playing recursive combat
            recursive_game = RecursiveGame(list(self.deck1)[:card1], list(self.deck2)[:card2])
            recursive_game.play_until_win()
            winner = recursive_game.winner
        else:
            # winner is determined by card
            winner = 1 if card1 > card2 else 2

        if winner == 1:
            self.deck1.extend([card1, card2])
        elif winner == 2:
            self.deck2.extend([card2, card1])

        if not self.deck1:
            self.winner = 2
        elif not self.deck2:
            self.winner = 1


def parse_decks(raw: str) -> Tuple[List[int], List[int]]:
    deck1_raw, deck2_raw = raw.strip().split('\n\n')
    deck1 = list(int(num) for num in deck1_raw.split('\n')[1:])
    deck2 = list(int(num) for num in deck2_raw.split('\n')[1:])
    return deck1, deck2


#
# Unit Tests
#

TEST_RAW = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

DECK1, DECK2 = parse_decks(TEST_RAW)
game = Game(DECK1, DECK2)
game.play_until_win()
assert game.winner_score() == 306

game = RecursiveGame(DECK1, DECK2)
game.play_until_win()
assert game.winner_score() == 291

#
# Problem
#
with open('inputs/22.txt') as file:
    RAW = file.read()

DECK1, DECK2 = parse_decks(RAW)
game = Game(DECK1, DECK2)
game.play_until_win()
print(game.winner_score())

game = RecursiveGame(DECK1, DECK2)
game.play_until_win()
print(game.winner_score())
