from abc import ABC, abstractmethod

from doku.grid import Grid


class Technique(ABC):
    name: str

    @abstractmethod
    def apply(self, grid: Grid) -> tuple[bool, Grid]:
        """Apply once; return True if it changed anything."""
