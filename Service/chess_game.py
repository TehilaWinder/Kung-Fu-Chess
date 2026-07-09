import config as cg
from Entities.board import Board
from Entities.move import Move
class Chess:
    def __init__(self, board):
        
        self.board = Board()
        self.is_valid_setup = self.board.load_and_validate(board)
        
        self.game_clock = 0
        self.is_game_over = False
        self.pending_moves = []  
        self.selected_piece_coords = None          

        
    def update_board(self):
        if self.is_game_over:
            return

        self.pending_moves.sort(key=lambda x: x.arrival_time)
        remaining_moves = []        
        for move in self.pending_moves:
             
            if move.arrival_time <= self.game_clock:
                dest_piece = self.board.execute_move(move)
                if dest_piece != cg.EMPTY_CELL and dest_piece.piece_type == 'K':
                    self.is_game_over = True
            else:
                remaining_moves.append(move)

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
            
            if not self.board.is_move_valid_on_board(piece, (r_src, c_src), (row, col)):
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
    def print_game(self):
        self.update_board()
        self.board.print_board()
            

    