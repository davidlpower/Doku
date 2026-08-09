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

    print(grid.matrix)
