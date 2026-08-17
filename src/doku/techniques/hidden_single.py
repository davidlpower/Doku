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

            # Skip if full row
            if len(empty_cells) > 0:
                for pv in possible_values:
                    for ec in list(empty_cells):
                        if len(empty_cells) == 1:
                            grid.set_cell_value(ec.row, ec.column, pv)
                            changed = True
                            break

                        values = grid.get_placed_for_column(ec.column) | grid.get_placed_for_column(ec.column)

                        if pv in values:
                            empty_cells.remove(ec)

        # Evaluate Columns
        # Evaluate Boxes
        return (changed, grid)
