from doku.cell import Cell


class Grid:
    def __init__(self, puzzle_string):
        w, h = 9, 9
        self.matrix = [[Cell(puzzle_string[h*w], []) for x in range(w)] for y in range(h)]
