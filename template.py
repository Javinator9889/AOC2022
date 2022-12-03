# Advent of Code - 2022 edition
# This file is a template: place it at "day**" and replace the specified function
from __future__ import annotations

import sys
import typing

from pathlib import Path

if typing.TYPE_CHECKING:
    ...


def advent(input: str) -> str:
    raise NotImplementedError("This method must be overridden")


if __name__ == "__main__":
    assert len(sys.argv) == 2, f"usage: {sys.argv[0]} INPUT_FILE"
    file = Path(sys.argv[1])

    assert file.exists(), f'input file "{file}" does not exist'
    assert file.is_file(), f'input file "{file}" is not a file'

    with file.open() as fd:
        print(advent(fd.read(())))

    sys.exit(0)
