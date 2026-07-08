import config as cg
from board import Board
from move import Move
from pieces import Queen
class Chess:
    def __init__(self, initial_board_lines):
        self.board = Board()
        self.is_valid_setup = self.board.load_and_validate(initial_board_lines)
        
        self.game_clock = 0
        self.is_game_over = False
        self.selected_piece_coords = None  
        self.pending_moves = []            

    def update_board(self):
        self.pending_moves.sort(key=lambda x: x.arrival_time)
        remaining_moves = []
        
        for move in self.pending_moves:
            if self.is_game_over:
                remaining_moves.append(move)
                continue
                
            if move.arrival_time > self.game_clock:
                remaining_moves.append(move)
                continue
            
            r_to, c_to = move.to_cell
            r_from, c_from = move.from_cell
            
            dest_piece = self.board.get_piece_at(r_to, c_to)
            
            if dest_piece == cg.EMPTY_CELL or dest_piece.color != move.piece.color:
                
                # בדיקת Game Over: אכילת מלך האויב
                if dest_piece != cg.EMPTY_CELL and dest_piece.piece_type == 'K':
                    self.is_game_over = True
                
                # ביצוע הצעד פיזית על הלוח
                self.board.set_piece_at(r_to, c_to, move.piece)
                
                
                # מחיקה מהמקור רק אם הכלי עדיין שם
                if self.board.get_piece_at(r_from, c_from) == move.piece:
                    self.board.set_piece_at(r_from, c_from, cg.EMPTY_CELL)
                if move.piece.piece_type == cg.PAWN:
                    if move.piece.color == cg.COLOR_WHITE and r_to==0 or move.piece.color == cg.COLOR_BLACK and r_to==self.board.height-1:
                        move.piece = Queen(move.piece.color, cg.PAWN_PROMOTION)
                        self.board.set_piece_at(r_to, c_to, move.piece)
            else:
                # התנגשות ידידותית - המהלך מבוטל (לא עושים כלום)
                pass
                
        self.pending_moves = remaining_moves

    def handle_click(self, row, col):
        
        if not self.board.is_within_bounds(row, col):
            return
            
        for move in self.pending_moves:
            if move.is_cell_in_path(row, col):
                self.selected_piece_coords = None  # ביטול בחירה ליתר ביטחון
                return

        # מצב א': בחירת כלי מקור (שום כלי עוד לא נבחר)
        
        if self.selected_piece_coords is None:
            if self.board.is_empty(row, col):
                return
            self.selected_piece_coords = (row, col)
            return

        # מצב ב': בחירת משבצת יעד ושליחת הכלי לתנועה
        else:
            r_src, c_src = self.selected_piece_coords
            piece = self.board.get_piece_at(r_src, c_src)
            
            if not piece.is_valid_step(self.board.grid, (r_src, c_src), (row, col)):
                self.selected_piece_coords = None
                return
                
         
            steps = max(abs(row - r_src), abs(col - c_src))
            travel_time = steps * cg.TIME_PER_CELL
            arrival_time = self.game_clock + travel_time
            
            new_move = Move((r_src, c_src), (row, col), piece, arrival_time)
            self.pending_moves.append(new_move)
            
            self.selected_piece_coords = None

    def advance_clock(self, time_to_wait):
        
        target_clock = self.game_clock + time_to_wait
        
        self.pending_moves.sort(key=lambda x: x.arrival_time)
        for move in list(self.pending_moves):
            if self.game_clock < move.arrival_time <= target_clock:
                self.game_clock = move.arrival_time
                self.update_board()
                if self.is_game_over:
                    return # נעצרנו בזמן אכילת המלך!
                    
        if not self.is_game_over:
            self.game_clock = target_clock