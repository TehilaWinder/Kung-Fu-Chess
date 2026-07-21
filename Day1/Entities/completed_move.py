from dataclasses import dataclass


@dataclass
class CompletedMove:
    """נתוני מהלך שהושלם - לוגיים בלבד, בלי מחרוזות/סמלים, לצריכת observers חיצוניים."""
    piece_type: str  # 'K'/'Q'/'R'/'B'/'N'/'P'
    color: str        # 'w' / 'b'
    from_cell: tuple  # (row, col)
    to_cell: tuple    # (row, col)
