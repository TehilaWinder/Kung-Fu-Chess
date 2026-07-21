# -*- coding: utf-8 -*-
"""
טסטים ליחידה Entities/Jump_action.py - מחלקת JumpAction בלבד.
"""
from Entities.Jump_action import JumpAction
from Entities.move import Move
from Entities.position import Position
from Entities.pieces import King, Rook


# ---------- is_expired ----------

def test_is_expired_false_before_landing_time():
    jump = JumpAction(King("w", "K"), 1, 1, landing_time=1000)
    assert jump.is_expired(999) is False


def test_is_expired_false_exactly_at_landing_time():
    # ב-JumpAction ה"תפיסה" תקפה עד וכולל landing_time - רק זמן מאוחר יותר פוקע
    jump = JumpAction(King("w", "K"), 1, 1, landing_time=1000)
    assert jump.is_expired(1000) is False


def test_is_expired_true_after_landing_time():
    jump = JumpAction(King("w", "K"), 1, 1, landing_time=1000)
    assert jump.is_expired(1001) is True


# ---------- intercepts ----------

def test_intercepts_true_when_enemy_move_lands_on_the_jump_cell():
    jump = JumpAction(King("w", "K"), 1, 1, landing_time=1000)
    enemy_move = Move(Position(0, 0), Position(1, 1), Rook("b", "R"), arrival_time=800, departure_time=0)
    assert jump.intercepts(enemy_move) is True


def test_intercepts_false_when_move_lands_on_a_different_cell():
    jump = JumpAction(King("w", "K"), 1, 1, landing_time=1000)
    move_elsewhere = Move(Position(0, 0), Position(2, 2), Rook("b", "R"), arrival_time=800, departure_time=0)
    assert jump.intercepts(move_elsewhere) is False


def test_intercepts_false_when_move_belongs_to_the_same_color():
    # קפיצה של כלי לבן לא "תופסת" מהלך של כלי לבן אחר שנוחת שם
    jump = JumpAction(King("w", "K"), 1, 1, landing_time=1000)
    friendly_move = Move(Position(0, 0), Position(1, 1), Rook("w", "R"), arrival_time=800, departure_time=0)
    assert jump.intercepts(friendly_move) is False
