from collections.abc import Iterable

from doku.cell import Cell


class Grid:
    def __init__(self, puzzle_string: str) -> None:
        self.w, self.h = 9, 9
        self.puzzle_string = puzzle_string
        self.matrix = []
        self.all_candidates = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.boxes = [
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
        # populate matrix
        for row in range(self.h):
            temp_row = []
            for column in range(self.w):
                value = self._get_value_from_puzzle_string(row, column)
                cell = Cell(value, set(), row, column)
                temp_row.append(cell)
            self.matrix.append(temp_row)

        # populate candidates
        self._refresh_candidates()

    def __str__(self) -> str:
        puzzle_string = self._to_puzzle_string()

        lines = []
        for row in range(self.h):
            if row != 0 and row % 3 == 0:
                lines.append("------+-------+------")

            row_values = []
            for column in range(self.w):
                if column != 0 and column % 3 == 0:
                    row_values.append("|")

                char = puzzle_string[row * self.w + column]
                row_values.append(char if char != "0" else ".")

            lines.append(" ".join(row_values))

        formatted_grid = "\n".join(lines)
        return f"\n\n{formatted_grid}\n\n{puzzle_string}"

    def _to_puzzle_string(self) -> str:
        chars = []
        for row in range(self.h):
            for column in range(self.w):
                value = self.matrix[row][column].value
                chars.append(str(value))
        return "".join(chars)

    def _refresh_candidates(self) -> None:
        # populate candidates
        for row in range(self.h):
            for column in range(self.w):
                if self.get_cell_value(row, column) == 0:
                    candidates = self.get_candidates_for_cell(row, column)
                    self.set_candidates_for_cell(row, column, candidates)
                else:
                    self.set_candidates_for_cell(row, column, set())

    def _get_placed(self, cells: Iterable[tuple[int, int]]) -> set[int]:
        placed = set()
        for row, column in cells:
            value = self.get_cell_value(row, column)
            if value != 0:
                placed.add(value)
        return placed

    def _get_value_from_puzzle_string(self, row: int, column: int) -> int:
        row_starts = [0, 9, 18, 27, 36, 45, 54, 63, 72]
        index = row_starts[row] + column
        return int(self.puzzle_string[index])

    def get_cell_value(self, row: int, column: int) -> int:
        cell = self.matrix[row][column]
        return cell.value

    def set_cell_value(self, row: int, column: int, value: int) -> None:
        self.matrix[row][column].value = value
        self.matrix[row][column].candidates = set()
        self._refresh_candidates()

    def get_empty_cells_for_row(self, row: int) -> set[Cell]:
        return {c for c in self.matrix[row] if c.value == 0}

    def get_remaining_values_for_row(self, row: int) -> set[int]:
        placed_values = self.get_placed_for_row(row)
        return self.all_candidates - placed_values

    def get_empty_cells_for_column(self, column: int) -> set[Cell]:
        return {row[column] for row in self.matrix if row[column].value == 0}

    def get_remaining_values_for_column(self, column: int) -> set[int]:
        placed_values = self.get_placed_for_column(column)
        return self.all_candidates - placed_values

    def get_remaining_values_for_box(self, row: int, column: int) -> set[int]:
        placed_values = self.get_placed_for_box(row, column)
        return self.all_candidates - placed_values

    def set_candidates_for_cell(self, row: int, column: int, candidates: set[int]) -> None:
        self.matrix[row][column].candidates = candidates

    def get_matrix_as_puzzle_string(self) -> str:
        puzzle_string = ""
        for row in range(self.h):
            for column in range(self.w):
                puzzle_string += str(self.get_cell_value(row, column))
        return puzzle_string

    def get_placed_for_row(self, row: int) -> set[int]:
        return self._get_placed((row, column) for column in range(self.w))

    def get_placed_for_column(self, column: int) -> set[int]:
        return self._get_placed((row, column) for row in range(self.h))

    def _get_box_for_row_column(self, row: int, column: int) -> int:
        identified_box = 0
        for index, box in enumerate(self.boxes):
            if row in box["rows"] and column in box["columns"]:
                identified_box = index
                break
        return identified_box

    def get_placed_for_box(self, row: int, column: int) -> set[int]:
        identified_box = self._get_box_for_row_column(row, column)
        placed = set()
        for row in self.boxes[identified_box]["rows"]:
            for column in self.boxes[identified_box]["columns"]:
                value = self.get_cell_value(row, column)
                if value != 0:
                    placed.add(value)
        return placed

    def get_empty_cells_for_box(self, row: int, column: int) -> set[Cell]:
        identified_box = self._get_box_for_row_column(row, column)
        empty_cells = set()
        for row in self.boxes[identified_box]["rows"]:
            for column in self.boxes[identified_box]["columns"]:
                cell = self.matrix[row][column]
                if cell.value == 0:
                    empty_cells.add(cell)
        return empty_cells

    def get_box_center_cells(self) -> set[tuple[int, int]]:
        return {(box["rows"][1], box["columns"][1]) for box in self.boxes}

    def get_candidates_for_cell(self, row: int, column: int) -> set[int]:
        # Guard Clause
        if self.get_cell_value(row, column) != 0:
            return set()

        values = self.get_placed_for_row(row) | self.get_placed_for_column(column) | self.get_placed_for_box(row, column)

        return self.all_candidates - values

    def get_cell_with_least_candidates(self) -> Cell:
        """Return the empty cell with the fewest candidate values.

        Used for the backtracking heuristic:
        guessing the most constrained cell first minimizes branching in the search tree.
        """
        return min((c for row in self.matrix for c in row if c.value == 0), key=lambda c: len(c.candidates))

    def is_solved(self) -> bool:
        all_values = []
        for row in range(self.h):
            for column in range(self.w):
                if self.get_cell_value(row, column) != 0:
                    all_values.append(self.get_cell_value(row, column))
        return len(all_values) == 81

    def is_invalid(self) -> bool:
        """ToDo"""
        return False
