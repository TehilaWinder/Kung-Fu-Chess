from dataclasses import dataclass


@dataclass
class Score:
    color: str
    score: int = 0

    def add_point(self):
        self.score += 1
