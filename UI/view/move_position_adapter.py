class MovePositionAdapter:
    def __init__(self, cell_size):
        self.cell_size = cell_size

    def get_pixel_position(self, move, clock) -> tuple[int, int]:
        """
        מחזיר מיקום פיקסל מדויק עם interpolation חלק בין שני segments סמוכים.
        בין segment[i] ל-segment[i+1] — interpolation לינארי לפי הזמן היחסי.
        """
        if not move.path:
            return move.from_cell.col * self.cell_size, move.from_cell.row * self.cell_size

        index = move.current_segment_index(clock)
        target = move.path[index]

        if index == 0:
            start_row, start_col, start_time = move.from_cell.row, move.from_cell.col, move.departure_time
        else:
            prev = move.path[index - 1]
            start_row, start_col, start_time = prev.row, prev.col, prev.arrival_time

        span = target.arrival_time - start_time
        pct = 1.0 if span == 0 else (clock - start_time) / span
        pct = max(0.0, min(1.0, pct))

        row = start_row + (target.row - start_row) * pct
        col = start_col + (target.col - start_col) * pct
        return int(col * self.cell_size), int(row * self.cell_size)
