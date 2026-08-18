import pytest

from doku.grid import Grid
from doku.techniques.hidden_single import HiddenSingle
from tests.conftest import SIMPLE_PUZZLE, SIMPLE_PUZZLE_SOLUTION


@pytest.mark.parametrize(
    ("puzzle", "expected"),
    [
        (SIMPLE_PUZZLE, True),
        (SIMPLE_PUZZLE_SOLUTION, False),
    ],
)
def test_technique_apply_correctly_reports_change(puzzle, expected) -> None:
    grid = Grid(puzzle)
    technique = HiddenSingle()
    actual, _updated_grid = technique.apply(grid)
    assert actual == expected

def test_hidden_single_correctly_finds_solution(simple_puzzle) -> None:
    expected = True
    grid = Grid(simple_puzzle)
    technique = HiddenSingle()
    changed, _updated_grid = technique.apply(grid)
    puzzle_string = _updated_grid.get_matrix_as_puzzle_string()
    assert simple_puzzle == puzzle_string
    assert changed == expected
