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

    def _apply_naked_pair(self, grid: Grid, empty_cells: list[Cell]) -> tuple[bool, Grid]:
        changed = False
        cell_pairs = itertools.combinations(empty_cells, r=2)

        for c1, c2 in cell_pairs:
            if len(c1.candidates) == 2 and c1.candidates == c2.candidates:
                naked_pair = c1.candidates
                empty_cells = [c for c in empty_cells if c is not c1 and c is not c2]
                matches = [ec for ec in empty_cells if naked_pair.intersection(grid.get_candidates_for_cell(ec.row, ec.column))]
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
            row_changed, grid = self._apply_naked_pair(grid, empty_cells)
            changed |= row_changed
        return (changed, grid)

    def _apply_for_column(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        for column in range(grid.w):
            empty_cells = grid.get_empty_cells_for_column(column)
            if len(empty_cells) < 2:
                continue
            column_changed, grid = self._apply_naked_pair(grid, empty_cells)
            changed |= column_changed
        return (changed, grid)

    def _apply_for_box(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        return (changed, grid)
