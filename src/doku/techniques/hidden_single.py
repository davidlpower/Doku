from doku.grid import Grid
from doku.techniques.technique import Technique


class HiddenSingle(Technique):
    name = "Naked Single"

    def apply(self, grid: Grid) -> tuple[bool, Grid]:
        changed = False
        # Evaluate Rows
        for row in range(grid.h):
            empty_cells = grid.get_empty_cells_for_row(row)
            possible_values = grid.get_remaining_values_for_row(row)
            # Skip complete row
            if len(empty_cells) > 0:
                for pv in possible_values:
                    for ec in list(empty_cells):
                        placed_values_row = grid.get_placed_for_column(ec.column)
                        placed_values_box = grid.get_placed_for_box(ec.row, ec.column)

                        # skip this itteration if value used already
                        if pv in placed_values_row or pv in placed_values_box:
                            continue

                        if len(empty_cells) == 1:
                            grid.set_cell_value(ec.row, ec.column, pv)
                            empty_cells.remove(ec)
                            changed = True
                            break

        # Evaluate Columns
        # Evaluate Boxes
        return (changed, grid)
