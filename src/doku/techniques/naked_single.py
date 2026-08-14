from doku.grid import Grid
from doku.techniques.technique import Technique


class NakedSingle(Technique):
    name = "Naked Single"

    def apply(self, grid: Grid) -> bool:
        return True
