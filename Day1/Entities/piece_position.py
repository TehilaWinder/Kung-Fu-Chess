from dataclasses import dataclass
from typing import Optional

from Entities.move import Move


@dataclass
class PiecePosition:
    piece_code: str          # e.g. "wP", "bK"
    state: str               # "idle" / "move" / "jump"
    since: float              # game_clock שממנו סופרים את זמן האנימציה של ה-state הזה
    row: float = 0.0          # מיקום לוגי - רלוונטי ל-"idle" ול-"jump"
    col: float = 0.0
    move: Optional[Move] = None  # רלוונטי ל-"move" בלבד - מסלול/תזמון להאצלת חישוב המיקום
