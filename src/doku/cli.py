import argparse
import copy

from doku.game_io import GameIO
from doku.grid import Grid
from doku.techniques.naked_single import NakedSingle


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

    techniques = [NakedSingle()]

    # stack holds grid "branches" to try. Starts with just the original grid.
    # Backtracking guesses get pushed here as new branches to explore later.
    stack = [grid]
    solved_grid = None

    backtrack_attempts = 0
    technique_attempts = 0
    # Keep taking branches off the stack until one solves, or we run out.
    while stack:
        grid = stack.pop()

        # Apply logic techniques repeatedly until none of them can make
        # any further progress on this grid
        while True:
            print("----Starting Main Loop----")
            progress = False
            for technique in techniques:
                print(f"-Starting {technique.name}-")
                changed, grid = technique.apply(grid)
                technique_attempts += 1
                if changed:
                    print("-Something changed-")
                    # Something changed - restart from the first technique,
                    # since earlier techniques may now apply again.
                    progress = True
                    break
                # This technique found nothing - try the next one.
                print("-Nothing Changed-")
                print(f"-Ending {technique.name}-")
            # A full pass over all techniques changed nothing: logic has
            # stalled (not necessarily solved, not necessarily wrong).
            if not progress:
                print("--No Progress Check--")
                break
        print("--[is_invalid Check]--")
        if grid.is_invalid():
            # This branch's guesses led somewhere impossible (e.g. a cell
            # with zero candidates left). Abandon it and try the next
            # branch on the stack.
            continue
        print("--[is_solved Check]--")
        if grid.is_solved():
            # Logic alone (possibly plus earlier guesses) finished the
            # puzzle. Stop entirely - no need to check remaining branches.
            solved_grid = grid
            break

        print("--Starting Backtrack--")
        # Logic stalled but the grid isn't solved or contradictory yet -
        # we have to guess. Pick the emptiest-looking cell (fewest
        # candidates) to minimise how many guesses we branch into.
        cell = grid.get_cell_with_least_candidates()

        # Push one new branch per possible value for that cell. These
        # get popped and processed (logic techniques + further guessing)
        # in later iterations of the outer while loop.
        for guess in cell.candidates:
            new_grid = copy.deepcopy(grid)
            new_grid.set_cell_value(cell.row, cell.column, guess)
            stack.append(new_grid)
            backtrack_attempts += 1

    if solved_grid is not None:
        print(solved_grid)
        print(f"Techniques: {technique_attempts} - Backtracks: {backtrack_attempts}")
    else:
        print("[No solution found]")
