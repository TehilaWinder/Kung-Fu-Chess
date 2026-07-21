# -*- coding: utf-8 -*-
"""
טסטים ליחידה Rules/move_rules.py - מחלקת MoveRules בלבד.
"""
from Rules.move_rules import MoveRules
from Entities.move import Move
from Entities.position import Position
from Entities.pieces import Rook


def make_pending_move(from_rc, to_rc, color="w", arrival_time=1000, departure_time=0):
    piece = Rook(color, "R")
    return Move(Position(*from_rc), Position(*to_rc), piece, arrival_time, departure_time)


# ---------- is_same_color ----------

def test_is_same_color_true_for_two_white_pieces():
    rules = MoveRules()
    assert rules.is_same_color(Rook("w", "R"), Rook("w", "N")) is True


def test_is_same_color_false_for_different_colors():
    rules = MoveRules()
    assert rules.is_same_color(Rook("w", "R"), Rook("b", "N")) is False


# ---------- has_pending_move_from ----------

def test_has_pending_move_from_true_when_that_cell_already_has_a_pending_move():
    rules = MoveRules()
    pending = [make_pending_move((0, 0), (0, 1))]
    assert rules.has_pending_move_from(pending, 0, 0) is True


def test_has_pending_move_from_false_when_a_different_cell_has_the_pending_move():
    rules = MoveRules()
    pending = [make_pending_move((0, 0), (0, 1))]
    assert rules.has_pending_move_from(pending, 0, 1) is False


def test_has_pending_move_from_false_when_nothing_is_pending():
    rules = MoveRules()
    assert rules.has_pending_move_from([], 0, 0) is False


# ---------- is_covered_by_pending_move ----------

def test_is_covered_by_pending_move_true_for_a_cell_on_a_pending_moves_path():
    rules = MoveRules()
    pending = [make_pending_move((0, 0), (0, 3))]
    assert rules.is_covered_by_pending_move(pending, 0, 2) is True


def test_is_covered_by_pending_move_false_for_a_cell_off_any_path():
    rules = MoveRules()
    pending = [make_pending_move((0, 0), (0, 3))]
    assert rules.is_covered_by_pending_move(pending, 5, 5) is False


# ---------- validate_move ----------

def test_validate_move_true_for_a_legal_step_with_no_conflicts(make_board):
    board = make_board("wR . .")
    rules = MoveRules()
    rook = board.get_piece_at(0, 0)
    assert rules.validate_move(board, [], rook, (0, 0), (0, 2)) is True


def test_validate_move_false_when_the_piece_cannot_legally_reach_the_target(make_board):
    board = make_board(
        "wR . .",
        ". . .",
    )
    rules = MoveRules()
    rook = board.get_piece_at(0, 0)
    assert rules.validate_move(board, [], rook, (0, 0), (1, 2)) is False


def test_validate_move_false_when_the_same_source_cell_already_has_a_pending_move(make_board):
    board = make_board("wR . .")
    rules = MoveRules()
    rook = board.get_piece_at(0, 0)
    pending = [make_pending_move((0, 0), (0, 1))]
    assert rules.validate_move(board, pending, rook, (0, 0), (0, 2)) is False


def test_validate_move_true_when_an_enemy_move_is_pending_from_a_different_cell(make_board):
    board = make_board("wR bN .")
    rules = MoveRules()
    rook = board.get_piece_at(0, 0)
    pending = [make_pending_move((0, 1), (0, 2), color="b")]
    assert rules.validate_move(board, pending, rook, (0, 0), (0, 1)) is True
