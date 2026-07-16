import config as cg
from Entities.path_segment import PathSegment
from Entities.pieces import Knight


class MoveRules:
    def is_same_color(self, piece, other_piece):
        return other_piece.color == piece.color

    def has_pending_move_from(self, pending_moves, row, col):
        return any(move.starts_from(row, col) for move in pending_moves)

    def is_covered_by_pending_move(self, pending_moves, row, col):
        return any(move.is_cell_in_path(row, col) for move in pending_moves)

    def validate_move(self, board, pending_moves, piece, from_cell, to_cell):
        if not board.is_move_valid_on_board(piece, from_cell, to_cell):
            return False
        if self.has_pending_move_from(pending_moves, *from_cell):
            return False
        return True

    def build_path(self, from_cell, to_cell, piece, departure_time) -> list[PathSegment]:
        """בונה את מסלול ה-segments של המהלך, ממוקד בזמן לפי TIME_PER_CELL."""
        r1, c1 = from_cell
        r2, c2 = to_cell
        delta_row = r2 - r1
        delta_col = c2 - c1
        steps = max(abs(delta_row), abs(delta_col))
        final_arrival_time = departure_time + steps * cg.TIME_PER_CELL

        if isinstance(piece, Knight):
            # הפרש קופץ ישר ליעד - אין תאים ביניים לבדוק
            return [PathSegment(r2, c2, final_arrival_time)]

        step_row = 0 if delta_row == 0 else (1 if delta_row > 0 else -1)
        step_col = 0 if delta_col == 0 else (1 if delta_col > 0 else -1)

        path = []
        for i in range(1, steps + 1):
            row = r1 + step_row * i
            col = c1 + step_col * i
            arrival_time = departure_time + i * cg.TIME_PER_CELL
            path.append(PathSegment(row, col, arrival_time))
        return path