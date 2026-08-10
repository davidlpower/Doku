import pytest

from doku.grid import Grid


@pytest.fixture
def standard_valid_incomplete() -> str:
    """81 Characters — one string of int characters"""
    return "000000000400056000006000950040008000092500801500190402300070090609000008080000100"

@pytest.fixture
def standard_valid_complete() -> str:
    """81 Characters — one string of int characters"""
    return "316578492529134768487629531263415987974863125851792643138947256692351874745286319"

def test_grid_initalisation(standard_valid_complete: str) -> None:
    grid = Grid(standard_valid_complete)
    assert grid.matrix is not None

@pytest.mark.parametrize(
    ("row", "column", "given_value"),
    [
        (0, 0, 3),
        (1, 1, 2),
        (2, 2, 7),
        (3, 3, 4),
        (4, 4, 6),
        (5, 5, 2),
        (6, 6, 2),
        (7, 7, 7),
        (8, 8, 9),
    ],
)
def test_extract_given_value_from_complete_puzzle_string(standard_valid_complete: str, row: int, column: int, given_value: int) -> None:
    grid = Grid(standard_valid_complete)
    expected_value = grid.extract_value_from_puzzle_string(row, column)
    assert  expected_value == given_value


@pytest.mark.parametrize(
    ("row", "column", "given_value"),
    [
        (0, 0, 0),
        (2, 1, 0),
        (6, 7, 9),
        (7, 7, 0),
    ],
)
def test_extract_given_value_from_incomplete_puzzle_string(standard_valid_incomplete: str, row: int, column: int, given_value: int) -> None:
    grid = Grid(standard_valid_incomplete)
    expected_value = grid.extract_value_from_puzzle_string(row, column)
    assert  expected_value == given_value
