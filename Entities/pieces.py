import config as cg


class Piece:
    def __init__(self, color, piece_type):
        self.color = color          # 'w' (לבן) או 'b' (שחור)
        self.piece_type = piece_type  # 'K', 'Q', 'R', 'B', 'N', 'P'
    def __str__(self):
        return f"{self.color}{self.piece_type}"

    def is_valid_step(self, board, from_cell, to_cell):
        raise NotImplementedError
    def promote(self, board_grid, to_cell):
        return self
    def check_blocking(self, board, from_cell, to_cell):
        
        r_prev, c_prev = from_cell
        r_new, c_new = to_cell
        delta_row = r_new - r_prev
        delta_col = c_new - c_prev

        step_row = 0 if delta_row == 0 else (1 if delta_row > 0 else -1)
        step_col = 0 if delta_col == 0 else (1 if delta_col > 0 else -1)

        current_row, current_col = r_prev + step_row, c_prev + step_col

        while (current_row, current_col) != (r_new, c_new):
            # אם התא אינו ריק (כלומר אינו ".")
            if not board.is_empty(current_row, current_col):
                return True
            current_row += step_row
            current_col += step_col

        return False

    def is_king(self):
        return self.piece_type == 'K'
    def can_capture(self, other_piece):
        return other_piece.color != self.color
# =====================================================================
# מחלקות הכלים הספציפיות - ירושה מ-Piece
# =====================================================================

class King(Piece):
    def __init__(self, color,p_type):
        super().__init__(color, p_type)

    def is_valid_step(self, board, from_cell, to_cell):
        r1, c1 = from_cell
        r2, c2 = to_cell
        delta_row = abs(r2 - r1)
        delta_col = abs(c2 - c1)
        # זז לכל היותר משבצת אחת לכל כיוון, וחובה לזוז
        return delta_row <= 1 and delta_col <= 1 and (delta_row > 0 or delta_col > 0)


class Rook(Piece):
    def __init__(self, color, p_type):
        super().__init__(color, p_type)

    def is_valid_step(self, board, from_cell, to_cell):
        r1, c1 = from_cell
        r2, c2 = to_cell
        delta_row = abs(r2 - r1)
        delta_col = abs(c2 - c1)
        if delta_row == 0 or delta_col == 0:
            return not self.check_blocking(board, from_cell, to_cell)
        return False


class Bishop(Piece):
    def __init__(self, color, p_type):
        super().__init__(color, p_type)

    def is_valid_step(self, board, from_cell, to_cell):
        r1, c1 = from_cell
        r2, c2 = to_cell
        # רץ זז רק באלכסונים
        if abs(r2 - r1) == abs(c2 - c1):
            return not self.check_blocking(board, from_cell, to_cell)
        return False


class Queen(Piece):
    def __init__(self, color, p_type):
        super().__init__(color, p_type)

    def is_valid_step(self, board, from_cell, to_cell):
        r1, c1 = from_cell
        r2, c2 = to_cell
        delta_row = abs(r2 - r1)
        delta_col = abs(c2 - c1)
        # מלכה משלבת את צריח ורץ
        if delta_row == 0 or delta_col == 0 or delta_row == delta_col:
            return not self.check_blocking(board, from_cell, to_cell)
        return False


class Knight(Piece):
    def __init__(self, color, p_type):
        super().__init__(color, p_type)

    def is_valid_step(self, board, from_cell, to_cell):
        r1, c1 = from_cell
        r2, c2 = to_cell
        delta_row = abs(r2 - r1)
        delta_col = abs(c2 - c1)
        # פרש נע בצורת L (אינו מושפע מחסימות בדרך)
        return (delta_row == 2 and delta_col == 1) or (delta_row == 1 and delta_col == 2)


class Pawn(Piece):
    def __init__(self, color, p_type):
        super().__init__(color, p_type)

    def is_valid_step(self, board, from_cell, to_cell):
        
        r1, c1 = from_cell
        r2, c2 = to_cell
        
        direction = -1 if self.color == cg.COLOR_WHITE else 1
        start_row = board.height - 1 if self.color == cg.COLOR_WHITE else 0
        delta_row = r2 - r1
        delta_col = abs(c2 - c1)
        if delta_col == 0 and  (delta_row==direction or (delta_row==2*direction and r1 == start_row)):
            if not board.is_empty(r2, c2):
                return False
            if delta_row == 2 * direction:
                if self.check_blocking(board, from_cell, to_cell):
                    return False
            return True
        
        if delta_col == 1 and delta_row == direction:
            target_piece = board.get_piece_at(r2, c2)
            if target_piece != cg.EMPTY_CELL and target_piece.color != self.color:
                return True
        return False

    def promote(self, board, to_cell):
        
        r2,_ = to_cell
        promotion_row = 0 if self.color == cg.COLOR_WHITE else board.height - 1

        if r2 == promotion_row:
            return Queen(self.color, 'Q')
        return self
    

TYPE_TO_CLASS = {
    'K': King,
    'Q': Queen,
    'R': Rook,
    'B': Bishop,
    'N': Knight,
    'P': Pawn
}