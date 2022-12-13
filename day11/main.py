# Advent of Code - 2022 edition
# This file is a template: place it at "day**" and replace the specified function
from __future__ import annotations

import sys
import typing
from enum import Enum
from pathlib import Path
from time import perf_counter

import numpy as np

try:
    from bfs import bfs, bfs_2
except ImportError:
    print("Cython module not available, ensure it has been compiled", file=sys.stderr)
    sys.exit(1)


if typing.TYPE_CHECKING:
    ...


class Part(Enum):
    P1 = "P1"
    P2 = "P2"


def advent_p1(input: str) -> str:
    mountain = np.genfromtxt(input.splitlines(), dtype=str, delimiter=1)
    view = mountain.view(np.int32)
    start_position = tuple(np.argwhere(mountain == "S")[0])
    end_position = tuple(np.argwhere(mountain == "E")[0])

    mountain[start_position] = "a"
    mountain[end_position] = "z"

    start = perf_counter()
    ret = bfs(view, start_position, end_position, False)
    end = perf_counter()
    print(f"elapsed: {end - start} ms")
    return ret


def advent_p2(input: str) -> str:
    mountain = np.genfromtxt(input.splitlines(), dtype=str, delimiter=1)
    view = mountain.view(np.int32)
    start_position = tuple(np.argwhere(mountain == "E")[0])
    end_position = tuple(np.argwhere(mountain == "S")[0])
    mountain[start_position] = "z"
    mountain[end_position] = "a"

    start = perf_counter()
    ret = bfs_2(view, start_position)
    end = perf_counter()
    print(f"elapsed: {end - start} ms")
    return ret


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
