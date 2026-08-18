import pytest

from doku.grid import Grid


@pytest.mark.parametrize(
    ("row", "column", "expected"),
    [
        (1, 0, 4),
        (4, 1, 9),
    ],
)
def test_get_cell_value_from_grid_matrix(easy_puzzle: str, row: int, column: int, expected: int) -> None:
    grid = Grid(easy_puzzle)
    actual = grid.get_cell_value(row, column)
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
def test_get_expected_value_from_complete(standard_valid_complete: str, row: int, column: int, expected: int) -> None:
    grid = Grid(standard_valid_complete)
    actual = grid.get_value_from_puzzle_string(row, column)
    assert actual == expected


@pytest.mark.parametrize(
    ("row", "column", "expected"),
    [
        (0, 0, 0),
        (1, 0, 4),
        (6, 7, 9),
        (8, 6, 1),
    ],
)
def test_get_expected_from_incomplete_puzzle_string(easy_puzzle: str, row: int, column: int, expected: int) -> None:
    grid = Grid(easy_puzzle)
    actual = grid.get_value_from_puzzle_string(row, column)
    assert actual == expected


def test_get_placed_for_given_column(easy_puzzle: str) -> None:
    expected = {5, 9, 7}
    column = 4
    grid = Grid(easy_puzzle)
    actual = grid.get_placed_for_column(column)
    assert actual == expected


def test_get_placed_for_given_row(easy_puzzle: str) -> None:
    expected = {3, 7, 9}
    row = 6
    grid = Grid(easy_puzzle)
    actual = grid.get_placed_for_row(row)
    assert actual == expected


@pytest.mark.parametrize(
    ("row", "column", "expected"),
    [
        (0, 0, {4, 6}),
        (1, 3, {5, 6}),
        (2, 6, {9, 5}),
        (3, 1, {2, 4, 5, 9}),
        (4, 4, {1, 5, 8, 9}),
        (5, 7, {1, 2, 4, 8}),
        (6, 2, {3, 6, 8, 9}),
        (7, 5, {7}),
        (8, 8, {1, 8, 9}),
    ],
)
def test_get_placed_for_given_box(easy_puzzle: str, row: int, column: int, expected: dict) -> None:
    grid = Grid(easy_puzzle)
    actual = grid.get_placed_for_box(row, column)
    assert actual == expected


def test_candidates_set_on_grid_init(easy_puzzle) -> None:
    given_row = 3
    given_column = 0
    expected_candidates = {1, 7}

    grid = Grid(easy_puzzle)
    actural_candidates = grid.get_candidates_for_cell(given_row, given_column)

    assert actural_candidates == expected_candidates


@pytest.mark.parametrize(
    ("row", "column"),
    [
        (1, 0),
        (1, 4),
        (2, 6),
        (4, 2),
        (5, 4),
        (5, 6),
        (8, 1),
        (6, 4),
        (7, 8),
    ],
)
def test_cell_with_value_has_no_candidates(easy_puzzle, row: int, column: int) -> None:
    expected_candidates = set()

    grid = Grid(easy_puzzle)
    actural_candidates = grid.get_candidates_for_cell(row, column)

    assert actural_candidates == expected_candidates


def test_get_cell_with_least_candidates(easy_puzzle) -> None:
    expected_row_column = (4, 0)
    grid = Grid(easy_puzzle)
    actural_cell = grid.get_cell_with_least_candidates()
    assert (actural_cell.row, actural_cell.column) == expected_row_column


def test_get_empty_cells_for_row(easy_puzzle) -> None:
    row = 4
    expected_cells = {(4, 0), (4, 4), (4, 5), (4, 7)}
    grid = Grid(easy_puzzle)
    actual_cells = grid.get_empty_cells_for_row(row)
    actual = {(cell.row, cell.column) for cell in actual_cells}
    assert actual == expected_cells


def test_get_remaining_values_for_row(easy_puzzle) -> None:
    row = 4
    expected_values = {3, 6, 7, 4}
    grid = Grid(easy_puzzle)
    actural_values = grid.get_remaining_values_for_row(row)
    assert actural_values == expected_values


def test_puzzle_with_empty_cells_is_not_solved(easy_puzzle) -> None:
    grid = Grid(easy_puzzle)
    expected = False
    actual = grid.is_solved()
    assert actual == expected


def test_puzzle_with_no_empty_cells_is_solved(standard_valid_complete) -> None:
    grid = Grid(standard_valid_complete)
    expected = True
    actual = grid.is_solved()
    assert actual == expected


def test_exported_puzzle_string_matches_given(easy_puzzle) -> None:
    grid = Grid(easy_puzzle)
    actual = grid.get_matrix_as_puzzle_string()
    assert actual == easy_puzzle
