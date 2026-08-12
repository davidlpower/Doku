from doku.cell import Cell


class Grid:
    def __init__(self, puzzle_string: str) -> None:
        self.w, self.h = 9, 9
        self.puzzle_string = puzzle_string
        self.matrix = []

        for row in range(self.h):
            temp_row = []
            for column in range(self.w):
                value = self.extract_value_from_puzzle_string(row, column)
                cell = Cell(value, set(), row, column)
                temp_row.append(cell)
            self.matrix.append(temp_row)

    def extract_value_from_puzzle_string(self, row: int, column: int) -> int:
        row_starts = [0, 9, 18, 27, 36, 45, 54, 63, 72]
        index = row_starts[row] + column
        return int(self.puzzle_string[index])

    def extract_value_from_matrix(self, row: int, column: int) -> int:
        cell = self.matrix[row][column]
        return cell.value

    def get_candidates_for_column(self, column: int) -> set[int]:
        candidates = set()

        for row in range(self.w):
            value = self.extract_value_from_matrix(row, column)
            if value != 0:
                candidates.add(value)

        return candidates

    def get_candidates_for_row(self, row: int) -> set[int]:
        candidates = set()

        for column in range(self.w):
            value = self.extract_value_from_matrix(row, column)
            if value != 0:
                candidates.add(value)

        return candidates

    def get_candidates_for_box(self, row: int, column: int) -> set[int]:
        boxes = [
            {"rows": [0,1,2], "cols": [0,1,2]}, {"rows": [0,1,2], "cols": [3,4,5]}, {"rows": [0,1,2], "cols": [6,7,8]},
            {"rows": [3,4,5], "cols": [0,1,2]}, {"rows": [3,4,5], "cols": [3,4,5]}, {"rows": [3,4,5], "cols": [6,7,8]},
            {"rows": [6,7,8], "cols": [0,1,2]}, {"rows": [6,7,8], "cols": [3,4,5]}, {"rows": [6,7,8], "cols": [6,7,8]},
        ]

        identified_box = 0
        for index, box in enumerate(boxes):
            if row in box["rows"] and column in box["cols"]:
                identified_box = index
                break

        candidates = set()
        for row in boxes[identified_box]["rows"]:
            for column in boxes[identified_box]["rows"]:
                value = self.extract_value_from_puzzle_string(row, column)
                if value != 0:
                    candidates.add(value)

        return candidates


# Jobs to be done
# - write a method to calculdate the possible candidates for a given cell
# - for Box, Row and Column
# - write a test that validates the candidates are correctly calculated
