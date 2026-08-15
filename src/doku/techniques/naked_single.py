from doku.grid import Grid
from doku.techniques.technique import Technique


class NakedSingle(Technique):
    name = "Naked Single"

    def apply(self, grid: Grid) -> tuple[bool, Grid]:
        # Loop over every cell
        changed = False
        for row in range(grid.h):
            for column in range(grid.w):
                candidates = grid.get_candidates_for_cell(row, column)
                if len(candidates) == 1:
                    (value,) = candidates
                    grid.set_cell_value(row, column, value)
                    changed = True
        return (changed, grid)
