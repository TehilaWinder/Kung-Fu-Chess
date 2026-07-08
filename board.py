import config as cg
from pieces import TYPE_TO_CLASS

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
                print("ERROR ROW_WIDTH_MISMATCH")
                return False
                
        self.grid = []
        
        for r in range(self.height):
            grid_row = []
            for c in range(self.width):
                token = board_lines[r][c]
                
                if token == cg.EMPTY_CELL:
                    grid_row.append(cg.EMPTY_CELL)
                    continue
                    
                if len(token) != 2 or token[0] not in (cg.COLOR_WHITE, cg.COLOR_BLACK) or token[1] not in cg.VALID_PIECE_TYPES:
                    print("ERROR UNKNOWN_TOKEN")
                    return False
                    
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
        """ מעדכנת כלי במשבצת מסוימת (או מוחקת על ידי השמת cg.EMPTY_CELL) """
        self.grid[row][col] = piece

    def is_within_bounds(self, row, col):
        """ בדיקה האם הקואורדינטות נמצאות בתוך גבולות הלוח """
        return 0 <= row < self.height and 0 <= col < self.width

    def print_board(self):
        for row in self.grid:
            # שימוש ב-str(cell) מפעיל אוטומטית את פונקציית __str__ של הכלים ומחזיר "wQ", "bK", "." וכו'
            row_str = [str(cell) for cell in row]
            print(' '.join(row_str))