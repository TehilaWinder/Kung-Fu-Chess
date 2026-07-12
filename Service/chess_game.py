import config as cg
from Entities.board import Board
from Entities.move import Move
from Entities.Jump_action import JumpAction
from Rules.move_rules import MoveRules
from Realtime.scheduler import Scheduler
class Chess:
    def __init__(self, board):

        self.board = Board()
        self.is_valid_setup = self.board.load_and_validate(board)

        self.is_game_over = False
        self.selected_piece_coords = None
        self.rules = MoveRules()
        self.scheduler = Scheduler()


    def update_board(self):
        if self.is_game_over:
            return
        if self.scheduler.update(self.board):
            self.is_game_over = True
            
    def handle_click(self, row, col):
        
        if not self.board.is_within_bounds(row, col):
            if self.selected_piece_coords is not None:
                self.selected_piece_coords = None
            return
            
        if self.rules.is_covered_by_pending_move(self.scheduler.pending_moves, row, col):
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
                if self.rules.is_same_color(piece, target_piece):
                    self.selected_piece_coords = (row, col)
                    return

            if not self.rules.validate_move(self.board, self.scheduler.pending_moves, piece, (r_src, c_src), (row, col)):
                self.selected_piece_coords = None
                return

            steps = max(abs(row - r_src), abs(col - c_src))
            travel_time = steps * cg.TIME_PER_CELL
            arrival_time = self.scheduler.game_clock + travel_time

            new_move = Move((r_src, c_src), (row, col), piece, arrival_time)
            self.scheduler.queue_move(new_move)

            self.selected_piece_coords = None

    def handle_jump(self, row, col):
        self.update_board()
        if self.board.is_empty(row, col):
            return

        if self.scheduler.has_pending_move_from(row, col):
            return

        piece = self.board.get_piece_at(row, col)

        jump_action = JumpAction(piece, row, col, self.scheduler.game_clock + 1000)
        self.scheduler.queue_jump(jump_action)

    def advance_clock(self, time_to_wait):
        if self.is_game_over:
            return
        if self.scheduler.advance(time_to_wait, self.board):
            self.is_game_over = True
            
    def print_game(self):
        self.update_board()
        self.board.print_board()
            

    