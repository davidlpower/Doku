from doku.cell import Cell


class Grid:
    def __init__(self, puzzle_string):
        w, h = 9, 9
        self.puzzle_string = puzzle_string
        self.matrix = []

        for row in range(h):
            temp_row = []
            for column in range(w):
                value = self.extract_value_from_puzzle_string(row, column)
                cell = Cell(value, [])
                temp_row.append(cell)
            self.matrix.append(temp_row)

    def extract_value_from_puzzle_string(self, row: int, column: int) -> int:
        row_starts = [0, 9, 18, 27, 36, 45, 54, 63, 72]
        index = row_starts[row] + column
        return int(self.puzzle_string[index])
