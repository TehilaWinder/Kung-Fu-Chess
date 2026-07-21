from dataclasses import dataclass


@dataclass
class PathSegment:
    row: int
    col: int
    arrival_time: float
