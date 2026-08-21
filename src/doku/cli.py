import argparse
import copy
import time
from pathlib import Path

from doku.game_io import GameIO
from doku.grid import Grid
from doku.techniques.hidden_single import HiddenSingle
from doku.techniques.naked_pair import NakedPair
from doku.techniques.naked_single import NakedSingle
from doku.telemetry import append_to_log, load_history, new_telemetry


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="Doku",
        description="Solves Soduko Puzzles",
    )
    parser.add_argument("path", help="path to the puzzle to solve")
    args = parser.parse_args(argv)

    game = GameIO()
    puzzle_string = game.load_puzzle(args.path)
    grid = Grid(puzzle_string)

    telemetry = new_telemetry(args.path)

    techniques = [NakedSingle(), HiddenSingle(), NakedPair()]

    # stack holds grid "branches" to try. Starts with just the original grid.
    # Backtracking guesses get pushed here as new branches to explore later.
    stack = [grid]
    solved_grid = None

    backtrack_attempts = 0
    technique_attempts = 0

    start = time.perf_counter()

    # Keep taking branches off the stack until one solves, or we run out.
    while stack:
        telemetry.max_stack_size = max(telemetry.max_stack_size, len(stack))
        grid = stack.pop()

        # Apply logic techniques repeatedly until none of them can make
        # any further progress on this grid
        while True:
            progress = False
            for technique in techniques:
                changed, grid = technique.apply(grid)
                technique_attempts += 1
                telemetry.record_technique(technique.name, changed)
                if changed:
                    # Something changed - restart from the first technique,
                    # since earlier techniques may now apply again.
                    progress = True
                    break
                # This technique found nothing - try the next one.

            # A full pass over all techniques changed nothing: logic has
            # stalled (not necessarily solved, not necessarily wrong).
            if not progress:
                break

        if not grid.is_valid():
            # This branch's guesses led somewhere impossible (e.g. a cell
            # with zero candidates left). Abandon it and try the next
            # branch on the stack.
            continue

        if grid.is_solved():
            # Logic alone (possibly plus earlier guesses) finished the
            # puzzle. Stop entirely - no need to check remaining branches.
            solved_grid = grid
            break

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

    # AI - TELEMETRY CODE BY AI
    telemetry.elapsed_seconds = time.perf_counter() - start
    telemetry.backtrack_attempts = backtrack_attempts
    telemetry.solved = solved_grid is not None
    append_to_log(telemetry, Path("telemetry") / "log.jsonl")

    if solved_grid is not None:
        print(solved_grid)
    else:
        print("[No solution found]")

    log_path = Path("telemetry") / "log.jsonl"
    history = load_history(log_path, args.path)
    print(f"\nHistory for {args.path} ({len(history)} run{'s' if len(history) != 1 else ''}):")
    for r in history:
        status = "solved" if r.solved else "failed"
        print(f"  {r.started_at}  {status:6}  {r.elapsed_seconds:.4f}s  backtracks={r.backtrack_attempts}")
        for name, stats in r.technique_stats.items():
            print(f"      {name}: {stats.successes}/{stats.attempts}")


# AI - TELEMETRY CODE BY AI
