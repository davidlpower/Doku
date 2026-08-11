class Cell:
    def __init__(self, value: int, candidates: set[int], row: int, column: int) -> None:
        self.value = value
        self.candidates = candidates
        self.row = row
        self.column = column
