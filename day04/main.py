# Advent of Code - 2022 edition
# This file is a template: place it at "day**" and replace the specified function
from __future__ import annotations

import sys
import typing

import numpy as np
import numpy.ma as ma

from collections import deque, namedtuple
from enum import Enum
from pathlib import Path

from lark import Lark

if typing.TYPE_CHECKING:
    ...


class Part(Enum):
    P1 = "P1"
    P2 = "P2"


# move <n> from <k> to <i>
parser = Lark.open("grammar.lark", rel_to=__file__, parser="lalr")
Moves = namedtuple("Moves", ("amount", "from_i", "to"))


def parse_input(input: str) -> tuple[list[deque[str]], list[Moves]]:
    matrix, moves = input.split("\n\n")
    # last line is only row numbers, we don't need it
    data = np.genfromtxt(
        matrix.splitlines(),
        delimiter=4,
        dtype=str,
        autostrip=True,
        skip_footer=True,
    )
    # we need to clean-up the matrix, so remove "[] ". In addition, we transpose
    # it so we have access to each crate per row, not per column. We also construct
    # a masked array for invalid values (in this case, empty ones). Thus it will be
    # easier to clean them up from Python lists.
    #
    # Note: we need stripped array to become an "object" array because string
    # comparison does not work for NumPy str ndtype
    data = ma.masked_equal(np.char.strip(data.T, "[]").astype(object), "")
    # Finally, create final list with all "None" values removed (masked arrays
    # return "None" for invalid values). We use "deque" because for pop/insert
    # operations is faster than lists
    data = [deque((value for value in row if value is not None)) for row in data.tolist()]

    moves_list: list[Moves] = []
    for move in moves.splitlines():
        tree = parser.parse(move)
        moves_list.append(Moves(*[int(child.value) for child in tree.children]))

    return data, moves_list


def advent_p1(input: str) -> str:
    """
    The expedition can depart as soon as the final supplies have been unloaded from the ships.
    Supplies are stored in stacks of marked crates, but because the needed supplies are buried
    under many other crates, the crates need to be rearranged.

    The ship has a giant cargo crane capable of moving crates between stacks. To ensure none
    of the crates get crushed or fall over, the crane operator will rearrange them in a series
    of carefully-planned steps. After the crates are rearranged, the desired crates will be at
    the top of each stack.

    The Elves don't want to interrupt the crane operator during this delicate procedure, but
    they forgot to ask her which crate will end up where, and they want to be ready to unload
    them as soon as possible so they can embark.

    They do, however, have a drawing of the starting stacks of crates and the rearrangement
    procedure (your puzzle input). For example::

            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2

    In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z
    is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top,
    they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

    Then, the rearrangement procedure is given. In each step of the procedure, a quantity of
    crates is moved from one stack to a different stack. In the first step of the above
    rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this
    configuration::

        [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

    In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one
    at a time, so the first crate to be moved (D) ends up below the second and third crates::

                [Z]
                [N]
            [C] [D]
            [M] [P]
         1   2   3

    Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one
    at a time, crate C ends up below crate M::

                [Z]
                [N]
        [M]     [D]
        [C]     [P]
         1   2   3

    Finally, one crate is moved from stack 1 to stack 2::

                [Z]
                [N]
                [D]
        [C] [M] [P]
         1   2   3

    The Elves just need to know which crate will end up on top of each stack; in this example,
    the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine
    these together and give the Elves the message CMZ.

    After the rearrangement procedure completes, what crate ends up on top of each stack?
    """
    crates, moves = parse_input(input)
    for move in moves:
        stack = crates[move.from_i - 1]
        picked = (stack.popleft() for _ in range(move.amount))
        crates[move.to - 1].extendleft(picked)

    res = []
    for crate in crates:
        res.append(crate.popleft())

    return "".join(res)


def advent_p2(input: str) -> str:
    raise NotImplementedError("This method must be overridden")


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
