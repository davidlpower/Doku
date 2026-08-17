import pytest

from doku.grid import Grid
from doku.techniques.hidden_single import HiddenSingle


@pytest.fixture
def puzzle() -> str:
    """
    9 . . | . 1 . | . . 3
    7 3 . | . 5 . | 1 8 6
    . 5 1 | 3 2 . | . . 4
    ------+-------+------
    . 9 . | . . . | 3 . 5
    3 4 . | 7 8 . | . 1 2
    1 . . | . 3 6 | 8 . .
    ------+-------+------
    2 6 . | . . 4 | 3 7 .
    5 . 8 | . 9 3 | . . .
    4 . 3 | . . . | 2 . .
    """
    return "900100003730050186051320004090000035340078012100036800260004370508093000403000200"


def test_naked_single_correctly_finds_solution(puzzle) -> None:
    grid = Grid(puzzle)
    technique = HiddenSingle()
    _changed, updated_grid = technique.apply(grid)

    assert updated_grid.get_matrix_as_puzzle_string() == puzzle_solution
