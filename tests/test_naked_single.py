import pytest

from conftest import EASY_PUZZLE, EASY_PUZZLE_SOLUTION
from doku.grid import Grid
from doku.techniques.naked_single import NakedSingle


@pytest.mark.parametrize(
    ("puzzle", "expected"),
    [
        (EASY_PUZZLE, True),
        (EASY_PUZZLE_SOLUTION, False),
    ],
)
def test_technique_apply_correctly_reports_change(puzzle, expected) -> None:
    grid = Grid(puzzle)
    technique = NakedSingle()
    actual, _updated_grid = technique.apply(grid)
    assert actual == expected


def test_naked_single_correctly_finds_solution(simple_puzzle, simple_puzzle_solution) -> None:
    grid = Grid(simple_puzzle)
    technique = NakedSingle()
    _changed, updated_grid = technique.apply(grid)

    assert updated_grid.get_matrix_as_puzzle_string() == simple_puzzle_solution
