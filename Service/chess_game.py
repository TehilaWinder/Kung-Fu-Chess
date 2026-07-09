import config as cg
from Entities.board import Board
from Entities.move import Move
from Entities.Jump_action import JumpAction
class Chess:
    def __init__(self, board):
        
        self.board = Board()
        self.is_valid_setup = self.board.load_and_validate(board)
        
        self.game_clock = 0
        self.is_game_over = False
        self.pending_moves = []  
        self.active_jumps = []
        self.selected_piece_coords = None          

        
    def update_board(self):
        if self.is_game_over:
            return
        self.active_jumps = [j for j in self.active_jumps if not j.is_expired(self.game_clock)]  # עכשיו בהתחלה
        self.pending_moves.sort(key=lambda x: x.arrival_time)
        remaining_moves = []
        for move in self.pending_moves:
            if move.arrival_time > self.game_clock:
                remaining_moves.append(move)
                continue
            if any(jump.intercepts(move) for jump in self.active_jumps):
                self.board.set_piece_at(*move.from_cell, cg.EMPTY_CELL)
                continue
            if self.board.resolve_arrival(move):
                self.is_game_over = True
        self.pending_moves = remaining_moves
            
    def handle_click(self, row, col):
        
        if not self.board.is_within_bounds(row, col):
            if self.selected_piece_coords is not None:
                self.selected_piece_coords = None
            return
            
        for move in self.pending_moves:
            if move.is_cell_in_path(row, col):
                self.selected_piece_coords = None  
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
            
            if not self.board.is_empty(row, col):
                target_piece = self.board.get_piece_at(row, col)
                if target_piece.color == piece.color:
                    self.selected_piece_coords = (row, col)
                    return
            
            if not self.board.is_move_valid_on_board(piece, (r_src, c_src), (row, col)):
                self.selected_piece_coords = None
                return
            
            if any(move.piece.color != piece.color for move in self.pending_moves):
                self.selected_piece_coords = None
                return

         
            steps = max(abs(row - r_src), abs(col - c_src))
            travel_time = steps * cg.TIME_PER_CELL
            arrival_time = self.game_clock + travel_time
            
            new_move = Move((r_src, c_src), (row, col), piece, arrival_time)
            self.pending_moves.append(new_move)
            
            self.selected_piece_coords = None
            
    def handle_jump(self, row, col):
        self.update_board()
        if self.board.is_empty(row, col):
            return

        if any(move.starts_from(row, col) for move in self.pending_moves):
            return

        piece = self.board.get_piece_at(row, col)

        jump_action = JumpAction(piece, row, col, self.game_clock + 1000)
        self.active_jumps.append(jump_action)
                        
                
        
    def advance_clock(self, time_to_wait):
        if self.is_game_over:
            return
            
        target_clock = self.game_clock + time_to_wait
        
        # 1. נאסוף את כל נקודות הזמן שבהן כלים אמורים להגיע בטווח הנוכחי
        arrival_times = {
            move.arrival_time for move in self.pending_moves 
            if self.game_clock < move.arrival_time <= target_clock
        }
        
        # 2. נוסיף את נקודת הסוף של ה-wait כתחנה מחייבת
        arrival_times.add(target_clock)
        
        # 3. נמיין את התחנות מהערך הנמוך לגבוה
        sorted_timeline = sorted(list(arrival_times))
        
        # 4. נתקדם בזמן תחנה אחר תחנה ונריץ עדכון לוח יחיד ומדויק לכל רגע
        for next_time in sorted_timeline:
            if self.is_game_over:
                break
            self.game_clock = next_time
            self.update_board()
            
    def print_game(self):
        self.update_board()
        self.board.print_board()
            

    