# Sudoku Solver

A Python CLI tool for solving classic 9×9 Sudoku puzzles using a **hybrid strategy**: logical constraint-propagation techniques first, falling back to backtracking search only when logic alone stalls. Difficulty rating falls out naturally, as a byproduct of tracking which techniques were needed to reach a solution.

## Goals

- Solve any valid 9×9 Sudoku puzzle correctly.
- Solve easy/medium puzzles using pure logic, no guessing.
- Fall back to backtracking + propagation for harder puzzles, without exploding in runtime.
- Report which technique(s) were used
- Clean, typed, testable Python

## Data Model

Each of the 81 cells is represented as a single `Cell` object holding both its value and its candidate set, rather than two parallel 9×9 arrays:

A `Grid.place(row, col, digit)` method is planned to handle placement atomically: set the value, clear that cell's candidates, and remove `digit` from the candidate sets of all peer cells (same row/column/box) in one step — keeping the "candidates always reflect current constraints" invariant automatically true after every placement.

## Solving Pipeline

### Stage 1 — Constraint Propagation (logic loop)

Applied repeatedly, in increasing order of complexity, until no technique makes progress:

1. Naked singles
2. Hidden singles
3. Naked pairs / triples

### Stage 2 — Backtracking Search

Triggered only if Stage 1 stalls with the puzzle unsolved:

- Choose the empty cell with the fewest remaining candidates (MRV heuristic).
- Try each candidate; after placing it, re-run Stage 1's propagation on the resulting grid before recursing (pruning the search space rather than doing naive brute force).
- On contradiction, backtrack.

### Stage 3 - Advanced Techniques

4. Pointing pairs (box–line reduction)
5. X-Wing
6. (Stretch) Swordfish, XY-Wing

## Stack

- **uv** for environment/dependency management
```bash
# Run a script/command inside the project's virtual environment
uv run doku ./tests/fixtures/sample1.txt
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
  - Property-based tests


### Pre-Commit 
```bash
uv run ruff check . --fix && uv run ruff format . && uv run mypy --strict src/ && uv run pytest
```

## Testing / Validation Strategy

- **Correctness**: every solved output must satisfy Sudoku constraints (`is_valid_solution(grid)`).
- **Technique isolation**: fixtures constructed so only technique X can fire, to verify each technique independently.
- **Performance**: track backtracking node count

## Milestones

1. **M1 — Grid + I/O**: data model, parsing from string/file, pretty-printing.
2. **M2 — Naked/hidden singles + backtracking fallback**: fully working end-to-end solver.
3. **M3 — Pairs/triples + pointing pairs**: reduces reliance on backtracking for medium puzzles.
4. **M4 — X-Wing and difficulty rating**: solves hard puzzles logically; rating output.
5. **M5 — CLI polish + benchmark suite**: usable tool, performance baseline established.

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