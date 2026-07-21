import config as cg
from UI.config.ui_config import BOARD_SIZE

_FILES = "abcdefgh"


def _cell_to_notation(row, col):
    """ ממירה (row, col) לוגי לתא בכתיב שחמט (a-h, 8-1). שייך ל-UI בלבד."""
    return f"{_FILES[col]}{BOARD_SIZE - row}"


class MoveLog:
    """Observer של Scheduler - הופך CompletedMove לוגי למחרוזת תצוגה, ושומר היסטוריה מוגבלת לכל צבע בנפרד."""

    MAX_ENTRIES = 20

    def __init__(self):
        self._entries_by_color = {
            cg.COLOR_WHITE: [],
            cg.COLOR_BLACK: [],
        }

    def entries_for(self, color):
        return self._entries_by_color[color]

    def on_move_completed(self, event):
        completed_move = event.data
        entries = self._entries_by_color[completed_move.color]
        entries.insert(0, self._format(completed_move))
        if len(entries) > self.MAX_ENTRIES:
            entries.pop()

    def _format(self, completed_move):
        piece_code = f"{completed_move.color}{completed_move.piece_type}"
        from_notation = _cell_to_notation(*completed_move.from_cell)
        to_notation = _cell_to_notation(*completed_move.to_cell)
        return f"{piece_code} {from_notation} -> {to_notation}"
