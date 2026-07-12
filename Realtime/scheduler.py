import config as cg


class Scheduler:
    def __init__(self):
        self.game_clock = 0
        self.pending_moves = []
        self.active_jumps = []

    def queue_move(self, move):
        self.pending_moves.append(move)

    def queue_jump(self, jump_action):
        self.active_jumps.append(jump_action)

    def has_pending_move_from(self, row, col):
        return any(move.starts_from(row, col) for move in self.pending_moves)

    def update(self, board):
        """מתקדמת רגע אחד: מפקיעה קפיצות שפג תוקפן ופותרת הגעות שהגיע זמנן.
        מחזירה True אם ההגעה הזו כללה אכילת מלך."""
        self.active_jumps = [j for j in self.active_jumps if not j.is_expired(self.game_clock)]
        self.pending_moves.sort(key=lambda x: x.arrival_time)

        remaining_moves = []
        king_captured = False
        for move in self.pending_moves:
            if not move.is_due(self.game_clock):
                remaining_moves.append(move)
                continue
            if any(jump.intercepts(move) for jump in self.active_jumps):
                board.set_piece_at(*move.from_cell, cg.EMPTY_CELL)
                continue
            if board.resolve_arrival(move):
                king_captured = True
        self.pending_moves = remaining_moves

        return king_captured

    def advance(self, time_to_wait, board):
        """מקדמת את השעון עד target_clock, עוצרת ב-update() בכל נקודת הגעה בדרך.
        מחזירה True אם בשלב כלשהו נאכל מלך."""
        target_clock = self.game_clock + time_to_wait

        arrival_times = {
            move.arrival_time for move in self.pending_moves
            if self.game_clock < move.arrival_time <= target_clock
        }
        arrival_times.add(target_clock)
        sorted_timeline = sorted(arrival_times)

        for next_time in sorted_timeline:
            self.game_clock = next_time
            if self.update(board):
                return True

        return False
