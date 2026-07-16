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
            self._resolve_dynamic_collisions(board)
            if self.update(board):
                return True

        return False

    def _segment_windows(self, move):
        """מחזירה לכל segment במסלול המהלך את חלון הזמן שבו הכלי נמצא בו."""
        windows = []
        prev_time = move.departure_time
        for segment in move.path:
            windows.append((segment, prev_time, segment.arrival_time))
            prev_time = segment.arrival_time
        return windows

    def _find_collision(self, move_a, move_b):
        """מוצאת זוג segments (אחד מכל מהלך) שחולקים אותו תא בחלון זמן חופף."""
        for seg_a, start_a, end_a in self._segment_windows(move_a):
            for seg_b, start_b, end_b in self._segment_windows(move_b):
                if (seg_a.row, seg_a.col) != (seg_b.row, seg_b.col):
                    continue
                if end_a < start_b or end_b < start_a:
                    continue
                return seg_a, seg_b
        return None

    def _eat_move(self, move, board):
        """הכלי שהיה בדרך נאכל - טרם הגיע ליעד, לכן פשוט מפנים את משבצת המקור."""
        board.set_piece_at(*move.from_cell, cg.EMPTY_CELL)

    def _freeze_move(self, move, board, collision_segment):
        """מקפיאה מהלך של כלי בן-צבע במשבצת הקודמת לזו שבה הייתה ההתנגשות."""
        index = move.path.index(collision_segment)
        if index == 0:
            frozen_row, frozen_col = move.from_cell
        else:
            prev_segment = move.path[index - 1]
            frozen_row, frozen_col = prev_segment.row, prev_segment.col

        board.set_piece_at(*move.from_cell, cg.EMPTY_CELL)
        board.set_piece_at(frozen_row, frozen_col, move.piece)

    def _resolve_dynamic_collisions(self, board):
        """בודקת כל זוג מהלכים ממתינים ומיישבת התנגשויות דינמיות לאורך המסלול."""
        resolved_ids = set()
        moves = self.pending_moves

        for i in range(len(moves)):
            move_a = moves[i]
            if id(move_a) in resolved_ids:
                continue
            for j in range(i + 1, len(moves)):
                move_b = moves[j]
                if id(move_b) in resolved_ids:
                    continue

                collision = self._find_collision(move_a, move_b)
                if collision is None:
                    continue
                seg_a, seg_b = collision

                if move_a.piece.color != move_b.piece.color:
                    if seg_a.arrival_time <= seg_b.arrival_time:
                        earlier = move_a
                    else:
                        earlier = move_b
                    self._eat_move(earlier, board)
                    resolved_ids.add(id(earlier))
                else:
                    if seg_a.arrival_time >= seg_b.arrival_time:
                        later, later_segment = move_a, seg_a
                    else:
                        later, later_segment = move_b, seg_b
                    self._freeze_move(later, board, later_segment)
                    resolved_ids.add(id(later))

        if resolved_ids:
            self.pending_moves = [m for m in self.pending_moves if id(m) not in resolved_ids]
