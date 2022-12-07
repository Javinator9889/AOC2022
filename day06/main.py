# Advent of Code - 2022 edition
# This file is a template: place it at "day**" and replace the specified function
from __future__ import annotations

import sys
import typing

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import cast, TypeVar

if typing.TYPE_CHECKING:
    from typing import Iterator


class Part(Enum):
    P1 = "P1"
    P2 = "P2"


@dataclass
class FileDescriptor(ABC):
    name: str = field()
    parent: Directory | None = field(default=None, init=False)

    @abstractmethod
    def mkcopy(self) -> FileDescriptor:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...


T = TypeVar("T", bound=FileDescriptor)


@dataclass
class File(FileDescriptor):
    size: int = field(default=0)

    def mkcopy(self) -> FileDescriptor:
        return File(self.name, self.size)

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"{self.name} (file, size={self.size})"


@dataclass
class Directory(FileDescriptor):
    contents: list[FileDescriptor] = field(default_factory=list)

    def addchild(self, o: FileDescriptor):
        o.parent = self
        self.contents.append(o)

    def mkcopy(self) -> Directory:
        d = Directory(self.name, self.contents.copy())
        d.parent = self.parent
        return d

    @property
    def indent_level(self) -> int:
        lvl = 0
        if self.parent is not None:
            lvl = self.parent.indent_level + 2

        return lvl

    def itertree(self) -> Iterator[tuple[str, FileDescriptor]]:
        dirname = self.name
        dirs: list[Directory] = []
        for content in self.contents:
            if isinstance(content, Directory):
                dirs.append(content)

            yield dirname, content

        for dir in dirs:
            yield from dir.itertree()

    def __len__(self) -> int:
        size = 0
        for file in self.contents:
            size += len(file)

        return size

    def __truediv__(self, o: T | str) -> T:
        if o in self:
            if isinstance(o, FileDescriptor):
                o = o.name

            for content in self.contents:
                if content.name == o:
                    return cast(T, content)

        if not isinstance(o, FileDescriptor):
            raise ValueError("Can only append child if it is a FileDescriptor")

        c = self.mkcopy()
        c.addchild(o)

        return o

    def __itruediv__(self, o: T | str) -> T | Directory:
        if o in self:
            if isinstance(o, FileDescriptor):
                o = o.name

            for content in self.contents:
                if content.name == o:
                    return cast(T, content)

        if not isinstance(o, FileDescriptor):
            raise ValueError("Can only append child if it is a FileDescriptor")

        self.addchild(o)
        return self

    def __contains__(self, o: FileDescriptor | str):
        if isinstance(o, FileDescriptor):
            o = o.name

        return o in {content.name for content in self.contents}

    def __repr__(self) -> str:
        contents = [f"{' ' * self.indent_level} - {self.name} (dir)"]
        for content in self.contents:
            prefix = f"{' ' * (self.indent_level + 2)} - " if not isinstance(content, Directory) else ""
            contents.append(f"{prefix}{repr(content)}")

        return "\n".join(contents)


def parse_tree(input: str) -> Directory:
    tree = Directory("/")
    cwd = tree
    for line in input.splitlines():
        if line.startswith("$"):
            data = line[2:].split()
            if data[0] == "cd":
                path = data[1]
                if path == "..":
                    if cwd.parent is not None:
                        cwd = cwd.parent
                else:
                    if path in cwd:
                        cwd /= path
        else:
            # line is the output of ls
            identifier, name = line.split()
            child: Directory | File
            if identifier == "dir":
                child = Directory(name)
            elif identifier.isdigit():
                child = File(name, int(identifier))
            else:
                raise ValueError(f'Unknown identifier "{identifier}"')

            cwd.addchild(child)

    return tree


def advent_p1(input: str) -> str:
    """You can hear birds chirping and raindrops hitting leaves as the expedition proceeds.
    Occasionally, you can even hear much louder sounds in the distance; how big do the
    animals get out here, anyway?

    The device the Elves gave you has problems with more than just its communication
    system. You try to run a system update::

        $ system-update --please --pretty-please-with-sugar-on-top
        Error: No space left on device

    Perhaps you can delete some files to make space for the update?

    You browse around the filesystem to assess the situation and save the resulting
    terminal output (your puzzle input). For example::

        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        dir e
        29116 f
        2557 g
        62596 h.lst
        $ cd e
        $ ls
        584 i
        $ cd ..
        $ cd ..
        $ cd d
        $ ls
        4060174 j
        8033020 d.log
        5626152 d.ext
        7214296 k

    The filesystem consists of a tree of files (plain data) and directories
    (which can contain other directories or files). The outermost directory is called /.
    You can navigate around the filesystem, moving into or out of directories and listing
    the contents of the directory you're currently in.

    Within the terminal output, lines that begin with $ are commands you executed,
    very much like some modern computers:

        * ``cd`` means change directory. This changes which directory is the current directory,
          but the specific result depends on the argument:
            * ``cd x`` moves in one level: it looks in the current directory for the directory
              named ``x`` and makes it the current directory.
            * ``cd ..`` moves out one level: it finds the directory that contains the current
              directory, then makes that directory the current directory.
            * ``cd /`` switches the current directory to the outermost directory, ``/``.
        * ``ls`` means list. It prints out all of the files and directories immediately
          contained by the current directory:
            * ``123 abc`` means that the current directory contains a file named abc with size 123.
            * ``dir xyz`` means that the current directory contains a directory named xyz.

    Given the commands and output in the example above, you can determine that the filesystem
    looks visually like this::

        - / (dir)
          - a (dir)
            - e (dir)
              - i (file, size=584)
            - f (file, size=29116)
            - g (file, size=2557)
            - h.lst (file, size=62596)
        - b.txt (file, size=14848514)
        - c.dat (file, size=8504156)
        - d (dir)
            - j (file, size=4060174)
            - d.log (file, size=8033020)
            - d.ext (file, size=5626152)
            - k (file, size=7214296)

    Here, there are four directories: / (the outermost directory), a and d (which are in /),
    and e (which is in a). These directories also contain files of various sizes.

    Since the disk is full, your first step should probably be to find directories that are
    good candidates for deletion. To do this, you need to determine the total size of each directory.
    The total size of a directory is the sum of the sizes of the files it contains, directly or
    indirectly. (Directories themselves do not count as having any intrinsic size.)

    The total sizes of the directories above can be found as follows:

        * The total size of directory e is 584 because it contains a single file i of size 584
          and no other directories.
        * The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and
          h.lst (size 62596), plus file i indirectly (a contains e which contains i).
        * Directory d has total size 24933642.
        * As the outermost directory, / contains every file. Its total size is 48381165, the sum
          of the size of every file.

    To begin, find all of the directories with a total size of at most 100000, then calculate the
    sum of their total sizes. In the example above, these directories are a and e; the sum of their
    total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

    Find all of the directories with a total size of at most 100000.
    What is the sum of the total sizes of those directories?
    """
    tree = parse_tree(input)

    # uncomment for pretty print tree
    # print(repr(tree))
    sizes: list[int] = []
    if (dir_len := len(tree)) <= 100000:
        sizes.append(dir_len)

    for _, file in tree.itertree():
        if isinstance(file, Directory):
            if (dir_len := len(file)) <= 100_000:
                sizes.append(dir_len)

    return f"{sum(sizes)}"


def advent_p2(input: str) -> str:
    """
    Now, you're ready to choose a directory to delete.

    The total disk space available to the filesystem is ``70000000``. To run the update, you need
    unused space of at least ``30000000``. You need to find a directory you can delete that will
    free up enough space to run the update.

    In the example above, the total size of the outermost directory (and thus the total amount
    of used space) is ``48381165``; this means that the size of the unused space must currently be
    ``21618835``, which isn't quite the ``30000000`` required by the update. Therefore, the update still
    requires a directory with total size of at least 8381165 to be deleted before it can run.

    To achieve this, you have the following options:

        * Delete directory ``e``, which would increase unused space by ``584``.
        * Delete directory ``a``, which would increase unused space by ``94853``.
        * Delete directory ``d``, which would increase unused space by ``24933642``.
        * Delete directory ``/,`` which would increase unused space by ``48381165``.

    Directories e and a are both too small; deleting them would not free up enough space.
    However, directories d and / are both big enough! Between these, choose the smallest: d,
    increasing unused space by ``24933642``.

    Find the smallest directory that, if deleted, would free up enough space on the
    filesystem to run the update. What is the total size of that directory?
    """
    tree = parse_tree(input)

    # uncomment for pretty print tree
    # print(repr(tree))
    tree_size = len(tree)
    available_space = 70_000_000
    unused_space = available_space - tree_size
    size_to_free = 30_000_000

    sizes: list[int] = []
    if unused_space + tree_size >= size_to_free:
        sizes.append(tree_size)

    for _, file in tree.itertree():
        if isinstance(file, Directory):
            if unused_space + (dir_len := len(file)) >= size_to_free:
                sizes.append(dir_len)

    return f"{min(sizes)}"


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
