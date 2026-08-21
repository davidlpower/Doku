from pathlib import Path


class GameIO:
    def load_puzzle(self, file_path: str) -> str:
        puzzle_string = ""
        if ".txt" in file_path:
            p = Path(file_path)
            with p.open() as f:
                puzzle_string = f.read()
        else:
            puzzle_string = file_path

        if self.validate_puzzle(puzzle_string):
            return puzzle_string
        raise Exception("Puzzle file exists but does not contain a valid puzzle")

    def validate_puzzle(self, puzzle: str) -> bool:
        return len(puzzle) == 81
