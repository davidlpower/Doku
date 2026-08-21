import itertools

from doku.cell import Cell
from doku.grid import Grid
from doku.techniques.technique import Technique


class NakedPair(Technique):
    name = "Naked Pair"

    def apply(self, grid: Grid) -> tuple[bool, Grid]:
        # Evaluate Row Candidates
        row_changed, grid = self._apply_for_row(grid)
        # Evaluate Columns Candidates
        column_changed, grid = self._apply_for_column(grid)
        # Evaluate Boxes Candidates
        box_changed, grid = self._apply_for_box(grid)

        return (row_changed | column_changed | box_changed, grid)

    def _apply_naked_pair(self, grid: Grid, remaining_empty_cells: list[Cell], naked_pair: set[int]) -> tuple[bool, Grid]:
        changed = False
        matches = [ec for ec in remaining_empty_cells if naked_pair.intersection(grid.get_candidates_for_cell(ec.row, ec.column))]
        if matches:
            for match in matches:
                # Did something actually happen here?
                updated_candidates = match.candidates - naked_pair
                # only update if there was a change
                if updated_candidates != match.candidates:
                    grid.set_candidates_for_cell(match.row, match.column, updated_candidates)
                    changed = True
        return (changed, grid)

    def _apply_for_row(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        for row in range(grid.h):
            empty_cells = grid.get_empty_cells_for_row(row)
            if len(empty_cells) < 2:
                continue

            cell_pairs = itertools.combinations(empty_cells, r=2)

            naked_pairs: set[int] = set()
            for c1, c2 in cell_pairs:
                if len(c1.candidates) == 2 and c1.candidates == c2.candidates:
                    naked_pairs = c1.candidates
                    remaining_empty_cells = [c for c in empty_cells if c is not c1 and c is not c2]
                    row_changed, grid = self._apply_naked_pair(grid, remaining_empty_cells, naked_pairs)
                    changed |= row_changed
                    break
        return (changed, grid)

    def _apply_for_column(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        return (changed, grid)

    def _apply_for_box(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        return (changed, grid)
