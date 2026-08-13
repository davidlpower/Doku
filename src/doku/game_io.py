from pathlib import Path


class GameIO:
    def load_puzzle_from_file(self, file_path: str) -> str:
        p = Path.open(file_path)
        with p as f:
            puzzle_string = f.read()
            if self.validate_puzzle(puzzle_string):
                return puzzle_string
            raise Exception("Puzzle file exists but does not contain a valid puzzle")

    def validate_puzzle(self, puzzle: str) -> bool:
        return len(puzzle) == 81
