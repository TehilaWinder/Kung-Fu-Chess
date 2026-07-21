# -*- coding: utf-8 -*-
"""
טסטים ליחידה Realtime/scheduler.py - מחלקת Scheduler בלבד.
בונים Board עם fixture make_board, אבל את הזמן/תורים מנהלים ישירות
דרך Scheduler בלי לעבור דרך Chess.handle_click/handle_jump.
"""
from Realtime.scheduler import Scheduler
from Entities.move import Move
from Entities.Jump_action import JumpAction
from Entities.position import Position
from Entities.pieces import Rook
from Rules.move_rules import MoveRules


def make_move(from_rc, to_rc, board, arrival_time, departure_time=0):
    piece = board.get_piece_at(*from_rc)
    return Move(Position(*from_rc), Position(*to_rc), piece, arrival_time, departure_time)


# ---------- queue_move / queue_jump / has_pending_move_from ----------

def test_queue_move_adds_it_to_pending_moves(make_board):
    scheduler = Scheduler()
    board = make_board("wR . .")
    move = make_move((0, 0), (0, 2), board, arrival_time=1000)
    scheduler.queue_move(move)
    assert scheduler.pending_moves == [move]


def test_queue_jump_adds_it_to_active_jumps(make_board):
    scheduler = Scheduler()
    board = make_board("wR . .")
    jump = JumpAction(board.get_piece_at(0, 0), 0, 0, landing_time=1000)
    scheduler.queue_jump(jump)
    assert scheduler.active_jumps == [jump]


def test_has_pending_move_from_true_for_the_moves_source_cell(make_board):
    scheduler = Scheduler()
    board = make_board("wR . .")
    scheduler.queue_move(make_move((0, 0), (0, 2), board, arrival_time=1000))
    assert scheduler.has_pending_move_from(0, 0) is True


def test_has_pending_move_from_false_when_nothing_is_pending():
    scheduler = Scheduler()
    assert scheduler.has_pending_move_from(0, 0) is False


# ---------- update ----------

def test_update_moves_a_due_piece_onto_the_board(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR . .")
    scheduler.queue_move(make_move((0, 0), (0, 2), board, arrival_time=0))
    scheduler.update(board, make_scores())
    assert board.is_empty(0, 0) is True
    assert board.get_piece_at(0, 2).piece_type == 'R'


def test_update_keeps_a_move_that_is_not_due_yet(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR . .")
    move = make_move((0, 0), (0, 2), board, arrival_time=1000)
    scheduler.queue_move(move)
    scheduler.update(board, make_scores())
    assert scheduler.pending_moves == [move]
    assert board.get_piece_at(0, 0).piece_type == 'R'  # עדיין לא זז


def test_update_returns_true_when_a_king_is_captured(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR bK .")
    scheduler.queue_move(make_move((0, 0), (0, 1), board, arrival_time=0))
    assert scheduler.update(board, make_scores()) is True


def test_update_returns_false_when_no_king_is_captured(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR . .")
    scheduler.queue_move(make_move((0, 0), (0, 2), board, arrival_time=0))
    assert scheduler.update(board, make_scores()) is False


def test_update_removes_expired_jumps(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wK . .")
    scheduler.queue_jump(JumpAction(board.get_piece_at(0, 0), 0, 0, landing_time=100))
    scheduler.game_clock = 101
    scheduler.update(board, make_scores())
    assert scheduler.active_jumps == []


def test_update_keeps_a_jump_that_has_not_expired(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wK . .")
    jump = JumpAction(board.get_piece_at(0, 0), 0, 0, landing_time=100)
    scheduler.queue_jump(jump)
    scheduler.game_clock = 100
    scheduler.update(board, make_scores())
    assert scheduler.active_jumps == [jump]


def test_update_lets_an_active_jump_intercept_an_enemy_move_landing_on_it(make_board, make_scores):
    # wK "קופצת" באוויר מעל המשבצת שלה עצמה (0,0); bR שמנסה לנחות שם
    # במהלך חלון הקפיצה נתפס באוויר ולא מגיע ליעד, וה-wK נשארת במקומה.
    scheduler = Scheduler()
    board = make_board("wK bR .")
    king = board.get_piece_at(0, 0)
    scheduler.queue_jump(JumpAction(king, 0, 0, landing_time=1000))
    scheduler.queue_move(make_move((0, 1), (0, 0), board, arrival_time=0))
    scheduler.update(board, make_scores())
    assert board.get_piece_at(0, 0) is king  # ה-wK נשארה במקומה, לא נאכלה
    assert board.is_empty(0, 1) is True      # ה-bR נתפסה באוויר ונעלמה ממקור התנועה
    assert scheduler.pending_moves == []


def test_update_awards_a_point_to_the_jumping_piece_that_intercepts(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wK bR .")
    king = board.get_piece_at(0, 0)
    scheduler.queue_jump(JumpAction(king, 0, 0, landing_time=1000))
    scheduler.queue_move(make_move((0, 1), (0, 0), board, arrival_time=0))
    scores = make_scores()
    scheduler.update(board, scores)
    assert scores["w"].score == 1
    assert scores["b"].score == 0


def test_update_awards_a_point_to_the_color_that_captures_on_arrival(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR bN .")
    scheduler.queue_move(make_move((0, 0), (0, 1), board, arrival_time=0))
    scores = make_scores()
    scheduler.update(board, scores)
    assert scores["w"].score == 1
    assert scores["b"].score == 0


def test_update_awards_no_point_when_a_move_lands_on_an_empty_cell(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR . .")
    scheduler.queue_move(make_move((0, 0), (0, 2), board, arrival_time=0))
    scores = make_scores()
    scheduler.update(board, scores)
    assert scores["w"].score == 0
    assert scores["b"].score == 0


# ---------- advance ----------

def test_advance_moves_the_clock_forward_by_the_requested_amount(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR . .")
    scheduler.advance(500, board, make_scores())
    assert scheduler.game_clock == 500


def test_advance_lands_a_move_that_becomes_due_within_the_wait(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR . .")
    scheduler.queue_move(make_move((0, 0), (0, 2), board, arrival_time=500))
    scheduler.advance(1000, board, make_scores())
    assert board.get_piece_at(0, 2).piece_type == 'R'
    assert scheduler.pending_moves == []


def test_advance_returns_true_as_soon_as_a_king_is_captured(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR bK .")
    scheduler.queue_move(make_move((0, 0), (0, 1), board, arrival_time=500))
    assert scheduler.advance(1000, board, make_scores()) is True


def test_advance_does_not_land_a_move_whose_arrival_is_still_in_the_future(make_board, make_scores):
    scheduler = Scheduler()
    board = make_board("wR . .")
    scheduler.queue_move(make_move((0, 0), (0, 2), board, arrival_time=2000))
    scheduler.advance(500, board, make_scores())
    assert board.get_piece_at(0, 0).piece_type == 'R'  # עוד לא נחת
    assert len(scheduler.pending_moves) == 1


def test_advance_awards_a_point_for_a_dynamic_collision_eat(make_board, make_scores):
    # wR: (0,4)->(8,4) בעמודה 4. bR: (4,0)->(4,8) בשורה 4 - חוצים מסלולים ב-(4,4) בזמן חופף.
    board = make_board(*([". . . . . . . . ."] * 9))
    wr = Rook("w", "R")
    br = Rook("b", "R")
    board.set_piece_at(0, 4, wr)
    board.set_piece_at(4, 0, br)

    rules = MoveRules()
    scheduler = Scheduler()
    scheduler.queue_move(Move(
        Position(0, 4), Position(8, 4), wr, arrival_time=8000, departure_time=0,
        path=rules.build_path((0, 4), (8, 4), wr, 0),
    ))
    scheduler.queue_move(Move(
        Position(4, 0), Position(4, 8), br, arrival_time=8000, departure_time=0,
        path=rules.build_path((4, 0), (4, 8), br, 0),
    ))

    scores = make_scores()
    scheduler.advance(8000, board, scores)
    assert scores["w"].score + scores["b"].score == 1
