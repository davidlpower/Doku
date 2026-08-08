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

A common misconception is that the solver picks a cell first and then chooses a technique to solve it. It doesn't — most techniques scan the **whole grid** for any place they apply, rather than targeting one pre-chosen cell.

```
loop:
    progress = false
    for technique in [naked_singles, hidden_singles, naked_pairs, pointing_pairs, x_wing, ...]:
        result = technique.apply(grid)   # scans ALL cells/units, not one cell
        if result made any change (filled a cell OR eliminated a candidate):
            grid = result
            progress = true
            break   # restart from the simplest technique again
    if not progress:
        break   # logic has stalled

if grid is fully solved:
    declare solved
else:
    run backtracking(grid)   # only now do we start "guessing" on a chosen cell
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

## Architecture / Module Layout

```
sudoku/
  grid.py            # Grid, Cell, Unit data structures
  io.py              # parse/serialize (string, file, common formats)
  techniques/
    singles.py
    pairs_triples.py
    pointing.py
    fish.py           # X-Wing, Swordfish
  propagate.py        # runs Stage 1 loop, aggregates techniques
  backtrack.py         # Stage 2 search
  solver.py            # public API: solve(grid) -> Solution
  rating.py             # Stage 3 difficulty scoring
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
- **Ruff** for linting/formatting
- **mypy --strict** for typing
- **pytest** for testing, including:
  - Unit tests per technique (hand-crafted grids isolating one pattern)
  - Integration tests against known puzzle sets of varying difficulty
  - Property-based tests (optional, via `hypothesis`) — e.g. "solved grid always satisfies all unit constraints"

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

## Open Questions

- How far to push technique coverage before backtracking is "good enough" (diminishing returns on rarer techniques like Swordfish/XY-Wing).
- Whether to support alternate puzzle sizes (4×4, 16×16) in the core data model now, even if unused in v1, to ease future extension.