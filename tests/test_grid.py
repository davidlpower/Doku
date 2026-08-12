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
    ("row", "column", "expected"),
    [
        (1, 0, 4),
        (4, 1, 9),
    ],
)
def test_extract_cell_value_from_grid_matrix(standard_valid_incomplete: str, row: int, column: int, expected: int) -> None:
    grid = Grid(standard_valid_incomplete)
    actual = grid.extract_value_from_matrix(row,column)
    assert expected == actual


@pytest.mark.parametrize(
    ("row", "column", "expected"),
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
def test_extract_expected_from_complete_puzzle_string(standard_valid_complete: str, row: int, column: int, expected: int) -> None:
    grid = Grid(standard_valid_complete)
    actual = grid.extract_value_from_puzzle_string(row, column)
    assert  actual == expected


@pytest.mark.parametrize(
    ("row", "column", "expected"),
    [
        (0, 0, 0),
        (1, 0, 4),
        (6, 7, 9),
        (8, 6, 1),
    ],
)
def test_extract_expected_from_incomplete_puzzle_string(standard_valid_incomplete: str, row: int, column: int, expected: int) -> None:
    grid = Grid(standard_valid_incomplete)
    actual = grid.extract_value_from_puzzle_string(row, column)
    assert  actual == expected


def test_get_candidates_for_given_column(standard_valid_incomplete: str) -> None:
    expected = {5,9,7}
    column = 4
    grid = Grid(standard_valid_incomplete)
    actual = grid.get_candidates_for_column(column)
    assert  actual == expected

def test_get_candidates_for_given_row(standard_valid_incomplete: str) -> None:
    expected = {3,7,9}
    row = 6
    grid = Grid(standard_valid_incomplete)
    actual = grid.get_candidates_for_row(row)
    assert  actual == expected

@pytest.mark.parametrize(
    ("row", "column", "expected"),
    [
        (1, 1, {4,6}),
        (3, 3, {1,5,8,9}),
        (7, 7, {1,8,9}),
    ],
)
def test_get_candidates_for_given_box(standard_valid_incomplete: str, row: int, column: int, expected: dict) -> None:
    grid = Grid(standard_valid_incomplete)
    actual = grid.get_candidates_for_box(row, column)
    assert  actual == expected
