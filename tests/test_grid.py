import pytest

from doku.grid import Grid


@pytest.fixture
def standard_valid_incomplete() -> str:
    """81 Characters — one string of . and int characters"""
    return ".........4...56.....6...95..4...8....925..8.15..19.4.23...7..9.6.9.....8.8....1.."

@pytest.fixture
def standard_valid_complete() -> str:
    """81 Characters — one string of . and int characters"""
    return "316578492529134768487629531263415987974863125851792643138947256692351874745286319"


def test_grid_initalisation(standard_valid_complete: str) -> None:
    grid = Grid(standard_valid_complete)
    assert grid.matrix is not None
