from abc import ABC, abstractmethod

from ..grid import Grid


class Technique(ABC):
    name: str

    @abstractmethod
    def apply(self, grid: Grid) -> bool:
        """Apply once; return True if it changed anything."""
