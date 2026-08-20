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

    def _apply_naked_pair(self):

        return

    def _apply_for_row(self):

        return

    def _apply_for_column(self):

        return

    def _apply_for_box(self):

        return
