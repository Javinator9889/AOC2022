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


def find_marker(input: str, view_length: int) -> int:
    for i in range(len(input) - view_length):
        view = input[i : i + view_length]
        if len(set(view)) == view_length:
            return i + view_length

    raise AttributeError("invalid input given")


def advent_p1(input: str) -> str:
    """
    The preparations are finally complete; you and the Elves leave camp on foot and begin to
    make your way toward the star fruit grove.

    As you move through the dense undergrowth, one of the Elves gives you a handheld device.
    He says that it has many fancy features, but the most important one to set up right now is
    the communication system.

    However, because he's heard you have significant experience dealing with signal-based systems,
    he convinced the other Elves that it would be okay to give you their one malfunctioning
    device - surely you'll have no problem fixing it.

    As if inspired by comedic timing, the device emits a few colorful sparks.

    To be able to communicate with the Elves, the device needs to lock on to their signal. The
    signal is a series of seemingly-random characters that the device receives one at a time.

    To fix the communication system, you need to add a subroutine to the device that detects a
    start-of-packet marker in the datastream. In the protocol being used by the Elves, the start of
    a packet is indicated by a sequence of four characters that are all different.

    The device will send your subroutine a datastream buffer (your puzzle input); your subroutine
    needs to identify the first position where the four most recently received characters were all
    different. Specifically, it needs to report the number of characters from the beginning of the
    buffer to the end of the first such four-character marker.

    For example, suppose you receive the following datastream buffer::

        mjqjpqmgbljsphdztnvjfqwrcgsmlb

    After the first three characters (mjq) have been received, there haven't been enough characters
    received yet to find the marker. The first time a marker could occur is after the fourth
    character is received, making the most recent four characters mjqj. Because j is repeated, this
    isn't a marker.

    The first time a marker appears is after the seventh character arrives. Once it does, the last
    four characters received are jpqm, which are all different. In this case, your subroutine
    should report the value 7, because the first start-of-packet marker is complete after 7
    characters have been processed.

    Here are a few more examples:

        * ``bvwbjplbgvbhsrlpgdmjqwftvncz``: first marker after character ``5``.
        * ``nppdvjthqldpwncqszvftbrmjlhg``: first marker after character ``6``.
        * ``nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg``: first marker after character ``10``.
        * ``zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw``: first marker after character ``11``.

    How many characters need to be processed before the first start-of-packet marker is detected?
    """
    return f"{find_marker(input, 4)}"


def advent_p2(input: str) -> str:
    """
    Your device's communication system is correctly detecting packets, but still isn't working.
    It looks like it also needs to look for messages.

    A start-of-message marker is just like a start-of-packet marker, except it consists of 14
    distinct characters rather than 4.

    Here are the first positions of start-of-message markers for all of the above examples:

        * ``mjqjpqmgbljsphdztnvjfqwrcgsmlb``: first marker after character ``19``.
        * ``bvwbjplbgvbhsrlpgdmjqwftvncz``: first marker after character ``23``.
        * ``nppdvjthqldpwncqszvftbrmjlhg``: first marker after character ``23``.
        * ``nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg``: first marker after character ``29``.
        * ``zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw``: first marker after character ``26``.

    How many characters need to be processed before the first start-of-message marker is detected?
    """
    return f"{find_marker(input, 14)}"


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
