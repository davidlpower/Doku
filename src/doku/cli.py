import argparse

from doku.game_io import GameIO
from doku.grid import Grid


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="Doku",
        description="Solves Soduko Puzzles",
    )
    parser.add_argument("path", help="path to the puzzle to solve")
    args = parser.parse_args(argv)

    game = GameIO()
    puzzle_string = game.load_puzzle_from_file(args.path)
    grid = Grid(puzzle_string)

    # Create instances of value Techniques
    # Create instances of candidate Techniques
    # Create Techniques array and populate

    # Loop Until the puzzle is solved.
        # loop over the techniques
        # Do technique on Cell
            # did it change anything
                # yes - continue
                # no  - move on
        # No Progress - logic stuck?
            # backtrack on cell with fewest candiates
    # Puzzle solved?

