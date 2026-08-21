import itertools

from doku.cell import Cell
from doku.grid import Grid
from doku.techniques.technique import Technique


class NakedTriple(Technique):
    name = "Naked Triple"

    def apply(self, grid: Grid) -> tuple[bool, Grid]:
        # Evaluate Row Candidates
        row_changed, grid = self._apply_for_row(grid)
        # Evaluate Columns Candidates
        column_changed, grid = self._apply_for_column(grid)
        # Evaluate Boxes Candidates
        box_changed, grid = self._apply_for_box(grid)

        return (row_changed | column_changed | box_changed, grid)

    def _apply_naked_triple(self, grid: Grid, empty_cells: set[Cell]) -> tuple[bool, Grid]:
        changed = False
        cell_triples = itertools.combinations(empty_cells, r=3)

        for c1, c2, c3 in cell_triples:
            union = c1.candidates | c2.candidates | c3.candidates
            # This is where the "Triple" check needs to happpen
            if len(union) == 3 and all(1 <= len(c.candidates) <= 3 for c in (c1, c2, c3)):
                # Must find the 3 candidates
                naked_triple = union
                empty_cells = {c for c in empty_cells if c is not c1 and c is not c2 and c is not c3}
                matches = {ec for ec in empty_cells if naked_triple.intersection(grid.get_candidates_for_cell(ec.row, ec.column))}
                if matches:
                    for match in matches:
                        # Did something actually happen here?
                        updated_candidates = match.candidates - naked_triple
                        # only update if there was a change
                        if updated_candidates != match.candidates:
                            grid.set_candidates_for_cell(match.row, match.column, updated_candidates)
                            changed = True
        return (changed, grid)

    def _apply_for_row(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        for row in range(grid.h):
            empty_cells = grid.get_empty_cells_for_row(row)
            if len(empty_cells) < 3:
                continue
            row_changed, grid = self._apply_naked_triple(grid, empty_cells)
            changed |= row_changed
        return (changed, grid)

    def _apply_for_column(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        for column in range(grid.w):
            empty_cells = grid.get_empty_cells_for_column(column)
            if len(empty_cells) < 3:
                continue
            column_changed, grid = self._apply_naked_triple(grid, empty_cells)
            changed |= column_changed
        return (changed, grid)

    def _apply_for_box(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        for box in grid.get_box_center_cells():
            empty_cells = grid.get_empty_cells_for_box(box[0], box[1])
            if len(empty_cells) < 3:
                continue
            box_changed, grid = self._apply_naked_triple(grid, empty_cells)
            changed |= box_changed
        return (changed, grid)
