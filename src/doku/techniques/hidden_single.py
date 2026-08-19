from doku.cell import Cell
from doku.grid import Grid
from doku.techniques.technique import Technique


class HiddenSingle(Technique):
    name = "Naked Single"

    def apply(self, grid: Grid) -> tuple[bool, Grid]:
        # Evaluate Rows
        row_changed, grid = self._apply_for_row(grid)
        # Evaluate Columns
        column_changed, grid = self._apply_for_column(grid)
        # Evaluate Boxes
        box_changed, grid = self._apply_for_box(grid)

        return (row_changed | column_changed | box_changed, grid)

    def _apply_hidden_single(self, grid: Grid, empty_cells: set[Cell], possible_values: set[int]) -> tuple[bool, Grid]:
        changed = False
        for pv in possible_values:
            matches = [
                ec for ec in empty_cells if
                pv in grid.get_candidates_for_cell(ec.row, ec.column)
            ]
            if len(matches) == 1:
                ec = matches[0]
                grid.set_cell_value(ec.row, ec.column, pv)
                changed = True
        return (changed, grid)

    def _apply_for_row(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        for row in range(grid.h):
            empty_cells = grid.get_empty_cells_for_row(row)
            if not empty_cells:
                continue
            possible_values = grid.get_remaining_values_for_row(row)
            row_changed, grid = self._apply_hidden_single(grid, empty_cells, possible_values)
            changed |= row_changed
        return (changed, grid)

    def _apply_for_column(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        for column in range(grid.w):
            empty_cells = grid.get_empty_cells_for_column(column)
            if not empty_cells:
                continue
            possible_values = grid.get_remaining_values_for_column(column)
            column_changed, grid = self._apply_hidden_single(grid, empty_cells, possible_values)
            changed |= column_changed
        return (changed, grid)

    def _apply_for_box(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        for box in grid.get_box_center_cells():
            empty_cells = grid.get_empty_cells_for_box(box[0], box[1])
            if not empty_cells:
                continue
            possible_values = grid.get_remaining_values_for_box(box[0], box[1])
            column_changed, grid = self._apply_hidden_single(grid, empty_cells, possible_values)
            changed |= column_changed
        return (changed, grid)
