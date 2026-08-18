import pytest

from doku.grid import Grid
from doku.techniques.hidden_single import HiddenSingle


def test_naked_single_correctly_finds_solution(simple_puzzle) -> None:
    expected = True
    grid = Grid(simple_puzzle)
    technique = HiddenSingle()
    changed, _updated_grid = technique.apply(grid)
    puzzle_string = _updated_grid.get_matrix_as_puzzle_string()
    assert simple_puzzle == puzzle_string
    assert changed == expected
