# Advent of Code - 2022 edition
# This file is a template: place it at "day**" and replace the specified function
from __future__ import annotations

import sys
import typing

from enum import Enum, IntEnum
from functools import reduce
from pathlib import Path

if typing.TYPE_CHECKING:
    ...


class Part(Enum):
    P1 = "P1"
    P2 = "P2"


class RPS(Enum):
    ROCK = "A"  # rock
    PAPER = "B"  # paper
    SCISSOR = "C"  # scissor

    def wins(self, o: RPS):
        if self is o:
            return False

        match self:
            case RPS.ROCK if o is RPS.SCISSOR:
                return True
            case RPS.PAPER if o is RPS.ROCK:
                return True
            case RPS.SCISSOR if o is RPS.PAPER:
                return True
            case _:
                return False

    @property
    def points(self):
        match self:
            case RPS.ROCK:
                return 1
            case RPS.PAPER:
                return 2
            case RPS.SCISSOR:
                return 3

    def fight(self, o: RPS) -> int:
        if self is o:
            return o.points + 3

        add = 6 if self.wins(o) else 0
        return self.points + add

    @classmethod
    def convert(cls, o: str) -> RPS:
        match o:
            case "X":
                return cls.ROCK
            case "Y":
                return cls.PAPER
            case "Z":
                return cls.SCISSOR
            case _:
                raise ValueError(f'Invalid character "{o}". Expected one of "X", "Y", "Z"')

    @classmethod
    def from_input(cls, line: str):
        a, o = line.split()
        # second "part" matches enum name, not value
        a, o = cls(a), cls.convert(o)
        return o.fight(a)


class RPSChooser(Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"

    def choose(self, o: RPS):
        if self is RPSChooser.DRAW:
            return o

        match o:
            case RPS.ROCK:
                if self is RPSChooser.LOSE:
                    return RPS.SCISSOR
                return RPS.PAPER
            case RPS.PAPER:
                if self is RPSChooser.LOSE:
                    return RPS.ROCK
                return RPS.SCISSOR
            case RPS.SCISSOR:
                if self is RPSChooser.LOSE:
                    return RPS.PAPER
                return RPS.ROCK

    @classmethod
    def from_input(cls, line: str):
        a, o = line.split()
        a, o = RPS(a), cls(o)

        o = o.choose(a)
        return o.fight(a)


def advent_p1(input: str) -> str:
    """
    The Elves begin to set up camp on the beach. To decide whose tent gets to be closest
    to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

    Rock Paper Scissors is a game between two players. Each game contains many rounds; in
    each round, the players each simultaneously choose one of Rock, Paper, or Scissors using
    a hand shape. Then, a winner for that round is selected: Rock defeats Scissors, Scissors
    defeats Paper, and Paper defeats Rock. If both players choose the same shape, the round
    instead ends in a draw.

    Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide
    (your puzzle input) that they say will be sure to help you win. "The first column
    is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors.
    The second column--" Suddenly, the Elf is called away to help with someone's tent.

    The second column, you reason, must be what you should play in response: X for Rock, Y
    for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses
    must have been carefully chosen.

    The winner of the whole tournament is the player with the highest score. Your total score
    is the sum of your scores for each round. The score for a single round is the score for
    the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for
    the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

    Since you can't be sure if the Elf is trying to help you or trick you, you should calculate
    the score you would get if you were to follow the strategy guide.

    For example, suppose you were given the following strategy guide::

        A Y
        B X
        C Z

    This strategy guide predicts and recommends the following:

        * In the first round, your opponent will choose Rock (A), and you should choose Paper (Y).
          This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
        * In the second round, your opponent will choose Paper (B), and you should choose Rock (X).
          This ends in a loss for you with a score of 1 (1 + 0).
        * The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.

    In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

    What would your total score be if everything goes exactly according to your strategy guide?
    """
    return sum(RPS.from_input(v) for v in input.splitlines())


def advent_p2(input: str) -> str:
    """The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says
    how the round needs to end: X means you need to lose, Y means you need to end the round in a draw,
    and Z means you need to win. Good luck!"

    The total score is still calculated in the same way, but now you need to figure out what shape to choose
    so the round ends as indicated. The example above now goes like this:

        * In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y),
          so you also choose Rock. This gives you a score of 1 + 3 = 4.
        * In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with
          a score of 1 + 0 = 1.
        * In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.

    Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

    Following the Elf's instructions for the second column, what would your total score be if everything goes
    exactly according to your strategy guide?
    """
    return sum(RPSChooser.from_input(v) for v in input.splitlines())


if __name__ == "__main__":
    assert len(sys.argv) in {2, 3}, f"usage: {sys.argv[0]} INPUT_FILE [P1/P2]"
    file = Path(sys.argv[1])
    part = Part(sys.argv[2]) if len(sys.argv) == 3 else Part.P1

    assert file.exists(), f'input file "{file}" does not exist'
    assert file.is_file(), f'input file "{file}" is not a file'

    with file.open() as fd:
        match part:
            case Part.P1:
                fn = advent_p1
            case Part.P2:
                fn = advent_p2
            case _:
                raise SystemError(f"Impossible pattern {part}")

        print(fn(fd.read()))

    sys.exit(0)
