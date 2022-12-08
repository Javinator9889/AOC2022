# Advent of Code - 2022 edition
# This file is a template: place it at "day**" and replace the specified function
from __future__ import annotations

import sys
import typing
from enum import Enum
from pathlib import Path

if typing.TYPE_CHECKING:
    ...


class Part(Enum):
    P1 = "P1"
    P2 = "P2"


def advent_p1(input: str) -> str:
    """
    The jungle must be too overgrown and difficult to navigate in vehicles
    or access from the air; the Elves' expedition traditionally goes on foot.
    As your boats approach land, the Elves begin taking inventory of their supplies.
    One important consideration is food - in particular, the number of Calories each
    Elf is carrying (your puzzle input).

    The Elves take turns writing down the number of Calories contained by the various meals,
    snacks, rations, etc. that they've brought with them, one item per line. Each Elf
    separates their own inventory from the previous Elf's inventory (if any) by a blank line.

    For example, suppose the Elves finish writing their items' Calories and end up with the
    following list::

        1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000

    This list represents the Calories of the food carried by five Elves:

        * The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000
          Calories.
        * The second Elf is carrying one food item with 4000 Calories.
        * The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
        * The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000
          Calories.
        * The fifth Elf is carrying one food item with 10000 Calories.

    In case the Elves get hungry and need extra snacks, they need to know which Elf to ask:
    they'd like to know how many Calories are being carried by the Elf carrying the most Calories.
    In the example above, this is 24000 (carried by the fourth Elf).

    Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
    """
    return max(
        (sum((int(calories) for calories in elf_data.split())) for elf_data in input.split("\n\n"))
    )


def advent_p2(input: str) -> str:
    """By the time you calculate the answer to the Elves' question, they've already realized
    that the Elf carrying the most Calories of food might eventually run out of snacks.

    To avoid this unacceptable situation, the Elves would instead like to know the total Calories
    carried by the top three Elves carrying the most Calories. That way, even if one of those
    Elves runs out of snacks, they still have two backups.

    In the example above, the top three Elves are the fourth Elf (with 24000 Calories),
    then the third Elf (with 11000 Calories), then the fifth Elf (with 10000 Calories).
    The sum of the Calories carried by these three elves is 45000.

    Find the top three Elves carrying the most Calories. How many Calories are those Elves
    carrying in total?
    """
    return sum(
        sorted(
            (
                sum((int(calories) for calories in elf_data.split()))
                for elf_data in input.split("\n\n")
            ),
            reverse=True,
        )[:3]
    )


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
