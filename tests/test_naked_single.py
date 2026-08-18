import pytest

from doku.grid import Grid
from doku.techniques.naked_single import NakedSingle


@pytest.mark.parametrize(
    ("puzzle", "expected"),
    [
        ("006078092529034760487629000263015987974003125851792643138900206692351874745006319", True),
        ("316578492529134768487629531263415987974863125851792643138947256692351874745286319", False),
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
