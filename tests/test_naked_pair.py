import pytest

from doku.grid import Grid
from doku.techniques.naked_pair import NakedPair
from tests.conftest import NAKED_PAIR_PUZZLE, NAKED_PAIR_SOLUTION


@pytest.mark.parametrize(
    ("puzzle", "expected"),
    [
        (NAKED_PAIR_PUZZLE, True),
        (NAKED_PAIR_SOLUTION, False),
    ],
)
def test_technique_apply_correctly_reports_change(puzzle, expected) -> None:
    grid = Grid(puzzle)
    technique = NakedPair()
    actual, _updated_grid = technique.apply(grid)
    assert actual == expected

