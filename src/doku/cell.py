class Cell:
    def __init__(self, value: int, candidates: set[int]) -> None:
        self.value = value
        self.candidates = candidates
