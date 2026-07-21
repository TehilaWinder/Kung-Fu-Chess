from dataclasses import dataclass


@dataclass
class PieceView:
    piece_code: str   # e.g. "wP", "bK"
    x: int            # pixel
    y: int            # pixel
    state: str        # "idle" / "move" / "jump"
    since: float       # game_clock שממנו סופרים את זמן האנימציה של ה-state הזה
