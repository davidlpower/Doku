from collections.abc import Iterable

from doku.cell import Cell


class Grid:
    def __init__(self, puzzle_string: str) -> None:
        self.w, self.h = 9, 9
        self.puzzle_string = puzzle_string
        self.matrix = []

        # populate matrix
        for row in range(self.h):
            temp_row = []
            for column in range(self.w):
                value = self.get_value_from_puzzle_string(row, column)
                cell = Cell(value, set(), row, column)
                temp_row.append(cell)
            self.matrix.append(temp_row)

        # populate candidatess
        for row in range(self.h):
            for column in range(self.w):
                candidates = self.get_candidates_for_cell(row, column)
                self.set_value_from_matrix(row, column, candidates)

    def get_value_from_puzzle_string(self, row: int, column: int) -> int:
        row_starts = [0, 9, 18, 27, 36, 45, 54, 63, 72]
        index = row_starts[row] + column
        return int(self.puzzle_string[index])

    def get_value_from_matrix(self, row: int, column: int) -> int:
        cell = self.matrix[row][column]
        return cell.value

    def set_value_from_matrix(self, row: int, column: int, candidates: set[int]) -> None:
        self.matrix[row][column].candidates = candidates

    def _get_placed(self, cells: Iterable[tuple[int, int]]) -> set[int]:
        placed = set()
        for row, column in cells:
            value = self.get_value_from_matrix(row, column)
            if value != 0:
                placed.add(value)
        return placed

    def get_placed_for_row(self, row: int) -> set[int]:
        return self._get_placed((row, column) for column in range(self.w))

    def get_placed_for_column(self, column: int) -> set[int]:
        return self._get_placed((row, column) for row in range(self.h))

    def get_placed_for_box(self, row: int, column: int) -> set[int]:
        boxes = [
            {"rows": [0, 1, 2], "columns": [0, 1, 2]},
            {"rows": [0, 1, 2], "columns": [3, 4, 5]},
            {"rows": [0, 1, 2], "columns": [6, 7, 8]},
            {"rows": [3, 4, 5], "columns": [0, 1, 2]},
            {"rows": [3, 4, 5], "columns": [3, 4, 5]},
            {"rows": [3, 4, 5], "columns": [6, 7, 8]},
            {"rows": [6, 7, 8], "columns": [0, 1, 2]},
            {"rows": [6, 7, 8], "columns": [3, 4, 5]},
            {"rows": [6, 7, 8], "columns": [6, 7, 8]},
        ]

        identified_box = None
        for index, box in enumerate(boxes):
            if row in box["rows"] and column in box["columns"]:
                identified_box = index
                break

        if identified_box is None:
            raise ValueError(f"No box found for row={row}, column={column}")

        placed = set()
        for row in boxes[identified_box]["rows"]:
            for column in boxes[identified_box]["columns"]:
                value = self.get_value_from_puzzle_string(row, column)
                if value != 0:
                    placed.add(value)

        return placed

    def get_candidates_for_cell(self, row: int, column: int) -> set[int]:
        all_candidates = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        values = self.get_placed_for_row(row) | self.get_placed_for_column(column) | self.get_placed_for_box(row, column)

        return all_candidates - values
