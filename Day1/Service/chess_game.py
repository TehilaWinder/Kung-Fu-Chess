import config as cg
from Entities.board import Board
from Entities.move import Move
from Entities.Jump_action import JumpAction
from Entities.position import Position
from Entities.score import Score
from Rules.move_rules import MoveRules
from Realtime.scheduler import Scheduler
from errors import BoardValidationError
class Chess:
    def __init__(self, board):

        self.board = Board()
        try:
            self.is_valid_setup = self.board.load_and_validate(board)
        except BoardValidationError as error:
            print(error)
            self.is_valid_setup = False

        self.is_game_over = False
        self.selected_piece_coords = None
        self.rules = MoveRules()
        self.scheduler = Scheduler()
        self.scores = {
            cg.COLOR_WHITE: Score(cg.COLOR_WHITE),
            cg.COLOR_BLACK: Score(cg.COLOR_BLACK),
        }


    def update_board(self):
        if self.is_game_over:
            return
        if self.scheduler.update(self.board, self.scores):
            self.is_game_over = True

    def get_winner(self):
        """מחזירה את צבע המלך שנשאר על הלוח, או None אם המשחק עוד לא נגמר."""
        if not self.is_game_over:
            return None
        for row in range(self.board.height):
            for col in range(self.board.width):
                piece = self.board.get_piece_at(row, col)
                if piece != cg.EMPTY_CELL and piece.is_king():
                    return piece.color
        return None

    def handle_click(self, row, col, color=None):
        if self.is_game_over:
            return

        if not self.board.is_within_bounds(row, col):
            if self.selected_piece_coords is not None:
                self.selected_piece_coords = None
            return

        # מצב א': בחירת כלי מקור (שום כלי עוד לא נבחר)

        if self.selected_piece_coords is None:
            if self.board.is_empty(row, col):
                return
            if color is not None and self.board.get_piece_at(row, col).color != color:
                return
            if self.rules.is_covered_by_pending_move(self.scheduler.pending_moves, row, col):
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
            departure_time = self.scheduler.game_clock

            path = self.rules.build_path((r_src, c_src), (row, col), piece, departure_time)

            new_move = Move(Position(r_src, c_src), Position(row, col), piece, arrival_time, departure_time, path)
            self.scheduler.queue_move(new_move)

            self.selected_piece_coords = None

    def handle_jump(self, row, col, color=None):
        if self.is_game_over:
            return
        if not self.board.is_within_bounds(row, col):
            return
        self.update_board()
        if self.board.is_empty(row, col):
            return

        if self.scheduler.has_pending_move_from(row, col):
            return

        piece = self.board.get_piece_at(row, col)

        if color is not None and piece.color != color:
            return

        jump_action = JumpAction(piece, row, col, self.scheduler.game_clock + 1000)
        self.scheduler.queue_jump(jump_action)

    def advance_clock(self, time_to_wait):
        if self.is_game_over:
            return
        if self.scheduler.advance(time_to_wait, self.board, self.scores):
            self.is_game_over = True
            
    def print_game(self):
        self.update_board()
        self.board.print_board()
            

    