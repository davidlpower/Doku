import pytest

from doku.grid import Grid
from doku.techniques.hidden_single import HiddenSingle
from tests.conftest import HIDDEN_SINGLE_PUZZLE, HIDDEN_SINGLE_SOLUTION


@pytest.mark.parametrize(
    ("puzzle", "expected"),
    [
        (HIDDEN_SINGLE_PUZZLE, True),
        (HIDDEN_SINGLE_SOLUTION, False),
    ],
)
def test_technique_apply_correctly_reports_change(puzzle, expected) -> None:
    grid = Grid(puzzle)
    technique = HiddenSingle()
    actual, _updated_grid = technique.apply(grid)
    assert actual == expected


def test_hidden_single_correctly_finds_solution(hidden_single_puzzle) -> None:
    apply_result = "601879043900506180000431069006390001009050600500007900160785390098003005375942816"
    grid = Grid(hidden_single_puzzle)
    technique = HiddenSingle()
    _changed, updated_grid = technique.apply(grid)
    updated_puzzle_string = updated_grid.get_matrix_as_puzzle_string()
    assert updated_puzzle_string == apply_result
