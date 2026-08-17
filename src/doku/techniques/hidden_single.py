from doku.grid import Grid
from doku.techniques.technique import Technique


class HiddenSingle(Technique):
    name = "Naked Single"

    def apply(self, grid: Grid) -> tuple[bool, Grid]:
        # Loop over every cell
        changed = False

        return (changed, grid)
