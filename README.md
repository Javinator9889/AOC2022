# AOC2022

This was my first Advent of Code, and I lasted until day 12 (mainly because of time concerns).
I really enjoyed this a lot, have to improve my programming skills and learn new algorithms,
which is always great.

At every folder you'll find the `main.py` Python file containing the source code (as well as
the day's problem as a docstring) and the entrypoint for running it.

The syntax is pretty straightforward:

```bash
python main.py <INPUT> [P1,P2]
```

where `P1` and `P2` refers to the first part and to the second part of the problem.

There are **some days** that are kind of special, such as `day11`, which is based on Cython
instead of using plain Python (you'll see there's a `Makefile` in there). Simply run `make` on
those and you'll be ready to proceed as usual.

## Dependencies
As there are some things that can be achieve easily using Python already exising libs (such
as NumPy), there are some dependencies required to run some day's problem. The simpler way
is to install [Poetry](https://python-poetry.org/) and run:

```bash
poetry install
```

That will automatically populate all dependencies for the project, create a `venv` for you
and prepare Python to be run.

The "long" way implies installing the dependencies with `pip`, by running:

```bash
pip install -r requirements.txt
```

### Python version
This project is intended to be run against **Python 3.11** or higher. It has not been tested against
Python prior such version (whereas it should run fine at least in **Python 3.10** because of `match`
statements).

Consider upgrading your Python version or deploy a virtual environment with such version or use a
Python version manager such as [`pyenv`](https://github.com/pyenv/pyenv).
