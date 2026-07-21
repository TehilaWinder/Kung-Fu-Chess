import config as cg
from Entities.piece_position import PiecePosition
from Entities.completed_move import CompletedMove
from Infrastructure.events import Event, MOVE_COMPLETED
from Infrastructure.event_bus import InMemoryEventBus


def _piece_code(piece):
    return piece.color + piece.piece_type


class Scheduler:
    def __init__(self, bus: InMemoryEventBus = None):
        self.game_clock = 0
        self.pending_moves = []
        self.active_jumps = []
        self.bus = bus if bus is not None else InMemoryEventBus()
        self._completed_moves = []  # מהלכים שהושלמו ב-update() האחרון, ממתינים לפרסום ב-advance()

    def queue_move(self, move):
        self.pending_moves.append(move)

    def queue_jump(self, jump_action):
        self.active_jumps.append(jump_action)

    def has_pending_move_from(self, row, col):
        return any(move.starts_from(row, col) for move in self.pending_moves)

    def get_visual_state(self, board) -> list[PiecePosition]:
        """מחזירה PiecePosition לכל כלי על הלוח - זז, קופץ או עומד.
        מיקומים לוגיים בלבד (row/col, או move לחישוב interpolation) - בלי פיקסלים."""
        positions = []
        seen_cells = set()

        for move in self.pending_moves:
            positions.append(PiecePosition(_piece_code(move.piece), "move", since=move.departure_time, move=move))
            seen_cells.add(tuple(move.from_cell))

        for jump in self.active_jumps:
            row, col = jump.cell.row, jump.cell.col
            if (row, col) in seen_cells:
                continue
            positions.append(PiecePosition(_piece_code(jump.piece), "jump", since=0, row=row, col=col))
            seen_cells.add((row, col))

        for row in range(board.height):
            for col in range(board.width):
                if (row, col) in seen_cells:
                    continue
                if board.is_empty(row, col):
                    continue
                piece = board.get_piece_at(row, col)
                positions.append(PiecePosition(_piece_code(piece), "idle", since=0, row=row, col=col))
                seen_cells.add((row, col))

        return positions

    def update(self, board, scores):
        """מתקדמת רגע אחד: מפקיעה קפיצות שפג תוקפן ופותרת הגעות שהגיע זמנן.
        מחזירה True אם ההגעה הזו כללה אכילת מלך."""
        self.active_jumps = [j for j in self.active_jumps if not j.is_expired(self.game_clock)]
        self.pending_moves.sort(key=lambda x: x.arrival_time)

        remaining_moves = []
        king_captured = False
        self._completed_moves = []
        for move in self.pending_moves:
            if not move.is_due(self.game_clock):
                remaining_moves.append(move)
                continue
            intercepting_jump = next((j for j in self.active_jumps if j.intercepts(move)), None)
            if intercepting_jump is not None:
                board.set_piece_at(*move.from_cell, cg.EMPTY_CELL)
                scores[intercepting_jump.piece.color].add_point()
                continue
            if board.resolve_arrival(move):
                king_captured = True
            if board.last_captured != cg.EMPTY_CELL:
                scores[move.piece.color].add_point()
            if board.is_empty(*move.from_cell):
                self._completed_moves.append(CompletedMove(
                    move.piece.piece_type, move.piece.color,
                    tuple(move.from_cell), tuple(move.to_cell),
                ))
        self.pending_moves = remaining_moves

        return king_captured

    def advance(self, time_to_wait, board, scores):
        """מקדמת את השעון עד target_clock, עוצרת ב-update() בכל נקודת הגעה בדרך.
        מודיעה ל-observers על כל מהלך שהגיע ליעדו. מחזירה True אם בשלב כלשהו נאכל מלך."""
        target_clock = self.game_clock + time_to_wait

        arrival_times = {
            move.arrival_time for move in self.pending_moves
            if self.game_clock < move.arrival_time <= target_clock
        }
        arrival_times.add(target_clock)
        sorted_timeline = sorted(arrival_times)

        for next_time in sorted_timeline:
            self.game_clock = next_time
            self._resolve_dynamic_collisions(board, scores)
            king_captured = self.update(board, scores)
            for completed_move in self._completed_moves:
                self.bus.publish(Event(MOVE_COMPLETED, completed_move))
            if king_captured:
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

    def _find_collision(self, move_a, move_b, clock):
        """מוצאת זוג segments (אחד מכל מהלך) שחולקים אותו תא בחלון זמן חופף -
        ושהחפיפה כבר התחילה בפועל (לא רק צפויה לקרות בעתיד)."""
        for seg_a, start_a, end_a in self._segment_windows(move_a):
            for seg_b, start_b, end_b in self._segment_windows(move_b):
                if (seg_a.row, seg_a.col) != (seg_b.row, seg_b.col):
                    continue
                if end_a < start_b or end_b < start_a:
                    continue
                if clock < max(start_a, start_b):
                    continue
                return seg_a, seg_b
        return None

    def _eat_move(self, move, board, scores, winner_color):
        """הכלי שהיה בדרך נאכל - טרם הגיע ליעד, לכן פשוט מפנים את משבצת המקור."""
        board.set_piece_at(*move.from_cell, cg.EMPTY_CELL)
        scores[winner_color].add_point()

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

    def _resolve_dynamic_collisions(self, board, scores):
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

                collision = self._find_collision(move_a, move_b, self.game_clock)
                if collision is None:
                    continue
                seg_a, seg_b = collision

                if move_a.piece.color != move_b.piece.color:
                    if seg_a.arrival_time <= seg_b.arrival_time:
                        earlier, winner = move_a, move_b
                    else:
                        earlier, winner = move_b, move_a
                    self._eat_move(earlier, board, scores, winner.piece.color)
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
