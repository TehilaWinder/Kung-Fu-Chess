class MoveRules:
    def is_same_color(self, piece, other_piece):
        return other_piece.color == piece.color

    def has_conflicting_pending_move(self, pending_moves, color):
        return any(move.piece.color != color for move in pending_moves)

    def is_covered_by_pending_move(self, pending_moves, row, col):
        return any(move.is_cell_in_path(row, col) for move in pending_moves)

    def validate_move(self, board, pending_moves, piece, from_cell, to_cell):
        if not board.is_move_valid_on_board(piece, from_cell, to_cell):
            return False
        if self.has_conflicting_pending_move(pending_moves, piece.color):
            return False
        return True