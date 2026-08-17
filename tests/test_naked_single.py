import pytest

from doku.grid import Grid
from doku.techniques.naked_single import NakedSingle


@pytest.fixture
def easy_puzzle() -> str:
    return "006078092529034760487629000263015987974003125851792643138900206692351874745006319"


@pytest.fixture
def easy_puzzle_solution() -> str:
    return "316578492529134768487629531263415987974863125851792643138947256692351874745286319"


@pytest.fixture
def naked_single_puzzle() -> str:
    return "530070000600195000098000060800060003400803001700020006060000280000419005000080079"


@pytest.fixture
def naked_single_puzzle_solution() -> str:
    return "534678912672195348198342567859761423426853791713924856961537284287419635345286179"


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


def test_naked_single_correctly_finds_solution(easy_puzzle, easy_puzzle_solution) -> None:
    grid = Grid(easy_puzzle)
    technique = NakedSingle()
    _changed, updated_grid = technique.apply(grid)

    assert updated_grid.get_matrix_as_puzzle_string() == easy_puzzle_solution
