# Sudoku Solver

A Python library and CLI tool for solving classic 9×9 Sudoku puzzles using a **hybrid strategy**: logical constraint-propagation techniques first, falling back to backtracking search only when logic alone stalls. Difficulty rating falls out naturally, as a byproduct of tracking which techniques were needed to reach a solution.

## Goals

- Solve any valid 9×9 Sudoku puzzle correctly.
- Solve easy/medium puzzles using pure logic, no guessing.
- Fall back to backtracking + propagation for harder puzzles, without exploding in runtime.
- Report which technique(s) were used, enabling a difficulty rating.
- Clean, typed, testable Python — reusable as a library, not just a script.

### Non-Goals (v1)

- Puzzle *generation* (planned as a follow-on project, reusing this solver).
- Variant Sudoku (Killer, Diagonal, irregular boxes, etc.) — architecture shouldn't preclude this later, but v1 targets classic 9×9.
- GUI — CLI and library API only.

## How Solving Works

```
def solve(grid: Grid) -> Grid | None:
    stack = [grid]

    while stack:
        grid = stack.pop()

        while True:
            progress = False
            for technique in TECHNIQUES:
                changed, grid = technique.apply(grid)
                if changed:
                    progress = True
                    break
            if not progress:
                break

        if grid.has_contradiction():
            continue  # dead end, try next item on stack

        if grid.is_solved():
            return grid

        cell = pick_cell_to_guess(grid)
        for guess in cell.candidates:
            new_grid = grid.copy()
            new_grid.place(cell, guess)
            stack.append(new_grid)

    return None  # stack exhausted, no solution
```

Key points:

- **No cell is chosen up front.** Each technique asks "can I make progress *anywhere* on the grid?"
- **Progress includes candidate elimination, not just filling in digits.** A technique like pointing pairs or X-Wing may remove a digit from several cells' candidate sets without placing any value — but that narrowing is still useful, since it can trigger a naked/hidden single elsewhere, cascading toward a solution without ever guessing.
- **After any progress, we restart from the cheapest techniques.** A single elimination can create a new naked single, so it's standard to retry cheap techniques before reaching for expensive ones again.
- **"All techniques failed" means a full pass made zero progress anywhere** — only then does backtracking kick in.
- **Backtracking is the one place a cell actually gets chosen** — typically the emptiest/most-constrained cell (fewest candidates, the MRV heuristic). After each guess, the full logic loop above re-runs on the resulting grid before deciding whether to guess again or backtrack.
- **Contradictions are caught immediately**, not just at the end — if a cell's candidate set ever drops to zero, or a unit can't fit a required digit, that's detected as soon as it happens.

## Data Model

Each of the 81 cells is represented as a single `Cell` object holding both its value and its candidate set, rather than two parallel 9×9 arrays:

```python
@dataclass
class Cell:
    value: int | None = None
    candidates: set[int] = field(default_factory=lambda: set(range(1, 10)))
    is_given: bool = False  # part of the original puzzle, immutable
```

Reasoning:

- **Data integrity.** A single object per cell makes it impossible for `value` and `candidates` to silently fall out of sync, which is easy to happen with two parallel arrays (e.g. updating one and forgetting the other).
- **Ergonomics for techniques.** Every technique reads and mutates cell state — a clean `Cell` API keeps that code simple and consistent across all technique implementations, rather than juggling coordinate-aligned arrays.
- **Extensibility.** `is_given` distinguishes original clues from solver-placed digits (needed so the solver never overwrites a clue, and useful later for puzzle generation). The object also gives a natural home for future metadata, like which technique solved a given cell (for difficulty rating/logging).

A `Grid.place(row, col, digit)` method is planned to handle placement atomically: set the value, clear that cell's candidates, and remove `digit` from the candidate sets of all peer cells (same row/column/box) in one step — keeping the "candidates always reflect current constraints" invariant automatically true after every placement.

## Solving Pipeline

### Stage 1 — Constraint Propagation (logic loop)

Applied repeatedly, in increasing order of complexity, until no technique makes progress:

1. Naked singles
2. Hidden singles
3. Naked pairs / triples
4. Pointing pairs (box–line reduction)
5. X-Wing
6. (Stretch) Swordfish, XY-Wing

Each technique is a pure function: `Grid -> (Grid, bool progress_made, TechniqueLog)`.

### Stage 2 — Backtracking Search

Triggered only if Stage 1 stalls with the puzzle unsolved:

- Choose the empty cell with the fewest remaining candidates (MRV heuristic).
- Try each candidate; after placing it, re-run Stage 1's propagation on the resulting grid before recursing (pruning the search space rather than doing naive brute force).
- On contradiction, backtrack.

### Stage 3 — Difficulty Rating (derived, not a separate solve)

Based on the techniques actually needed to reach a solution:

- **Easy** — singles only.
- **Medium** — + pairs/triples, pointing pairs.
- **Hard** — + X-Wing or similar.
- **Expert/Extreme** — backtracking required at all.

## Example Architecture / Module Layout

```
sudoku/
  grid.py            # Grid, Cell, Unit data structures
  io.py              # parse/serialize (string, file, common formats)
  techniques/
    singles.py
    pairs_triples.py
    pointing.py
    fish.py           # X-Wing, Swordfish
  cli.py                 # command-line entry point
tests/
  fixtures/               # puzzles by known difficulty, for regression
  test_techniques/
  test_backtrack.py
  test_solver_integration.py
```

## Public API (sketch)

```python
from sudoku import solve

result = solve(puzzle_string)
result.solved: bool
result.grid: Grid
result.techniques_used: list[TechniqueName]
result.difficulty: Difficulty
result.backtrack_steps: int  # 0 if pure logic
```

## Tech Stack

- **uv** for environment/dependency management
```bash
# Run a script/command inside the project's virtual environment
uv run python src/doku/io.py
uv run pytest
```
- **Ruff** for linting/formatting
```bash
# Lint the project (reports style/error violations)
uv run ruff check .
# Check formatting without changing files (useful in CI)
uv run ruff format --check .
```
- **mypy --strict** for typing
```bash
# Type-check the whole project in strict mode
uv run mypy --strict src/
```
- **pytest** for testing, including:
  - Unit tests per technique (hand-crafted grids isolating one pattern)
  - Integration tests against known puzzle sets of varying difficulty
  - Property-based tests (optional, via `hypothesis`) — e.g. "solved grid always satisfies all unit constraints"


### Possible Pre-Commit 
```bash
uv run ruff check . --fix && uv run ruff format . && uv run mypy --strict src/ && uv run pytest
```

## Testing / Validation Strategy

- **Correctness**: every solved output must satisfy Sudoku constraints (`is_valid_solution(grid)`).
- **Technique isolation**: fixtures constructed so only technique X can fire, to verify each technique independently.
- **Difficulty regression**: a fixed set of puzzles with known human-assigned difficulty, checked against the solver's derived rating.
- **Performance**: track backtracking node count / wall-clock time on a "hardest known" puzzle (e.g. Arto Inkala's 2012 puzzle) as a benchmark.

## Milestones

1. **M1 — Grid + I/O**: data model, parsing from string/file, pretty-printing.
2. **M2 — Naked/hidden singles + backtracking fallback**: fully working end-to-end solver.
3. **M3 — Pairs/triples + pointing pairs**: reduces reliance on backtracking for medium puzzles.
4. **M4 — X-Wing and difficulty rating**: solves hard puzzles logically; rating output.
5. **M5 — CLI polish + benchmark suite**: usable tool, performance baseline established.
6. **(Future) M6 — Puzzle generation**: reuse solver for uniqueness-checking during generation.

# Techniques:

Types of Techniques

## Place a value directly

- Naked singles - cell has one candidate left → fill it in.
- Hidden singles - candidate has one legal cell in a unit → fill it in.
- Backtracking - guesses a value into a cell with the fewest candidates (then propagates/backtracks on contradiction).

## Only narrow candidates (never place a value directly)

- Naked pairs/triples
- Hidden pairs/triples
- Pointing pairs/triples (box-line reduction)
- X-Wing
- Swordfish/Jellyfish
- Simple coloring / X-Cycles
- XY-Wing / XYZ-Wing
- AIC

All of these only eliminate candidates from the cells candidate sets. They never directly solve a cell. They work indirectly: by eliminating enough candidates, they can create a new naked or hidden single, which is what actually places the value on the next loop.

# Solver logic
- Scan the whole board for naked singles (any cell, no unit needed), place any found.
- If none found, scan unit by unit (each row, each column, each box) for hidden singles, place any found.
- If a value was placed in step 1 or 2, go back to step 1 and repeat, since the new placement will have removed that value from other cells' candidate lists and may have created new singles.
- If neither step finds anything, escalate to the next technique (pairs/triples, etc.).