import config as cg
from Entities.pieces import TYPE_TO_CLASS
from errors import RowWidthMismatchError, UnknownTokenError

class Board:
    def __init__(self):
        self.grid = []  
        self.height = 0
        self.width = 0
    

    def load_and_validate(self, board_lines):
        
        if not board_lines:
            return False
            
        self.height = len(board_lines)
        self.width = len(board_lines[0])
        
        for row in board_lines:
            if len(row) != self.width:
                raise RowWidthMismatchError()
                
        self.grid = []
        
        for r in range(self.height):
            grid_row = []
            for c in range(self.width):
                token = board_lines[r][c]
                
                if token == cg.EMPTY_CELL:
                    grid_row.append(cg.EMPTY_CELL)
                    continue
                    
                if len(token) != 2 or token[0] not in (cg.COLOR_WHITE, cg.COLOR_BLACK) or token[1] not in cg.VALID_PIECE_TYPES:
                    raise UnknownTokenError()
                    
                color = token[0]
                p_type = token[1]
                
                piece_class= TYPE_TO_CLASS[p_type]
                piece_obj=piece_class(color,p_type)
                grid_row.append(piece_obj)
                
            self.grid.append(grid_row)
            
        return True

    def is_empty(self, row, col):
        return self.grid[row][col] == cg.EMPTY_CELL

    def get_piece_at(self, row, col):
        """ מחזירה את אובייקט הכלי שנמצא במשבצת, או cg.EMPTY_CELL אם ריק """
        return self.grid[row][col]

    def set_piece_at(self, row, col, piece):
        
        self.grid[row][col] = piece

    def is_within_bounds(self, row, col):
        """ בדיקה האם הקואורדינטות נמצאות בתוך גבולות הלוח """
        return 0 <= row < self.height and 0 <= col < self.width
    
    def execute_move(self, move):
        r_from, c_from = move.from_cell
        r_to, c_to = move.to_cell
        
        captured_piece = self.get_piece_at(r_to, c_to)
        
        self.set_piece_at(r_from, c_from, cg.EMPTY_CELL)
        
        
        promoted_piece = move.piece.promote(self, move.to_cell)
            
        self.set_piece_at(r_to, c_to, promoted_piece)
        
            
        return captured_piece
    def resolve_arrival(self, move):
        """מנסה לבצע נחיתה של move. מחזירה True אם התוצאה היא אכילת מלך."""
        dest_piece = self.get_piece_at(*move.to_cell)
        if dest_piece != cg.EMPTY_CELL and not move.piece.can_capture(dest_piece):
            return False  # התנגשות ידידותית — לא מבוצע כלום
        captured = self.execute_move(move)
        return captured != cg.EMPTY_CELL and captured.is_king()

    def is_move_valid_on_board(self, piece, from_cell, to_cell):
        
        return piece.is_valid_step(self, from_cell, to_cell)

    def print_board(self):
        for row in self.grid:
            row_str = [str(cell) for cell in row]
            print(' '.join(row_str))