# -*- coding: utf-8 -*-
"""
טסטים ליחידה Entities/board.py - מחלקת Board בלבד (בלי scheduler/Chess).
"""
import pytest

import config as cg
from Entities.board import Board
from Entities.move import Move
from Entities.position import Position
from Entities.pieces import Rook, Pawn, King
from errors import RowWidthMismatchError, UnknownTokenError


# ---------- load_and_validate ----------

def test_load_and_validate_true_for_a_well_formed_board(make_board):
    board = make_board("wR . .", ". . .")
    assert board.height == 2
    assert board.width == 3


def test_load_and_validate_places_the_right_piece_type_and_color(make_board):
    board = make_board("wR bN .")
    assert isinstance(board.get_piece_at(0, 0), Rook)
    assert board.get_piece_at(0, 0).color == cg.COLOR_WHITE
    assert board.get_piece_at(0, 1).color == cg.COLOR_BLACK


def test_load_and_validate_false_for_empty_input():
    board = Board()
    assert board.load_and_validate([]) is False


def test_load_and_validate_raises_when_row_widths_differ():
    board = Board()
    with pytest.raises(RowWidthMismatchError):
        board.load_and_validate([["wR", ".", "."], [".", "."]])


def test_load_and_validate_raises_for_unknown_token():
    board = Board()
    with pytest.raises(UnknownTokenError):
        board.load_and_validate([["xZ", "."]])


# ---------- is_empty / get_piece_at / set_piece_at ----------

def test_is_empty_true_for_a_dot_cell(make_board):
    board = make_board(". . .")
    assert board.is_empty(0, 1) is True


def test_is_empty_false_for_an_occupied_cell(make_board):
    board = make_board("wR . .")
    assert board.is_empty(0, 0) is False


def test_set_piece_at_overwrites_the_cell(make_board):
    board = make_board(". . .")
    rook = Rook("w", "R")
    board.set_piece_at(0, 1, rook)
    assert board.get_piece_at(0, 1) is rook


# ---------- is_within_bounds ----------

def test_is_within_bounds_true_for_a_cell_inside_the_grid(make_board):
    board = make_board(". . .", ". . .")
    assert board.is_within_bounds(1, 2) is True


def test_is_within_bounds_false_for_negative_coordinates(make_board):
    board = make_board(". . .")
    assert board.is_within_bounds(-1, 0) is False


def test_is_within_bounds_false_for_coordinates_past_the_edge(make_board):
    board = make_board(". . .")
    assert board.is_within_bounds(0, 3) is False


# ---------- execute_move ----------

def test_execute_move_clears_the_source_cell(make_board):
    board = make_board("wR . .")
    move = Move(Position(0, 0), Position(0, 2), board.get_piece_at(0, 0), arrival_time=0, departure_time=0)
    board.execute_move(move)
    assert board.is_empty(0, 0) is True


def test_execute_move_places_the_piece_on_the_destination_cell(make_board):
    board = make_board("wR . .")
    piece = board.get_piece_at(0, 0)
    move = Move(Position(0, 0), Position(0, 2), piece, arrival_time=0, departure_time=0)
    board.execute_move(move)
    assert board.get_piece_at(0, 2) is piece


def test_execute_move_returns_the_piece_that_was_captured(make_board):
    board = make_board("wR bR .")
    captured_should_be = board.get_piece_at(0, 1)
    move = Move(Position(0, 0), Position(0, 1), board.get_piece_at(0, 0), arrival_time=0, departure_time=0)
    captured = board.execute_move(move)
    assert captured is captured_should_be


def test_execute_move_returns_empty_cell_when_destination_was_empty(make_board):
    board = make_board("wR . .")
    move = Move(Position(0, 0), Position(0, 2), board.get_piece_at(0, 0), arrival_time=0, departure_time=0)
    captured = board.execute_move(move)
    assert captured == cg.EMPTY_CELL


def test_execute_move_promotes_a_pawn_that_reaches_the_last_row(make_board):
    board = make_board(". . .", "wP . .")
    pawn = board.get_piece_at(1, 0)
    move = Move(Position(1, 0), Position(0, 0), pawn, arrival_time=0, departure_time=0)
    board.execute_move(move)
    assert board.get_piece_at(0, 0).piece_type == 'Q'


# ---------- resolve_arrival ----------

def test_resolve_arrival_moves_the_piece_when_destination_is_empty(make_board):
    board = make_board("wR . .")
    piece = board.get_piece_at(0, 0)
    move = Move(Position(0, 0), Position(0, 2), piece, arrival_time=0, departure_time=0)
    board.resolve_arrival(move)
    assert board.get_piece_at(0, 2) is piece
    assert board.is_empty(0, 0) is True


def test_resolve_arrival_does_nothing_on_friendly_collision(make_board):
    board = make_board("wR wN .")
    rook = board.get_piece_at(0, 0)
    knight = board.get_piece_at(0, 1)
    move = Move(Position(0, 0), Position(0, 1), rook, arrival_time=0, departure_time=0)
    board.resolve_arrival(move)
    # שני הכלים נשארים בדיוק איפה שהיו - שום דבר לא בוצע
    assert board.get_piece_at(0, 0) is rook
    assert board.get_piece_at(0, 1) is knight


def test_resolve_arrival_returns_false_when_no_king_was_captured(make_board):
    board = make_board("wR bN .")
    move = Move(Position(0, 0), Position(0, 1), board.get_piece_at(0, 0), arrival_time=0, departure_time=0)
    assert board.resolve_arrival(move) is False


def test_resolve_arrival_returns_true_when_a_king_is_captured(make_board):
    board = make_board("wR bK .")
    move = Move(Position(0, 0), Position(0, 1), board.get_piece_at(0, 0), arrival_time=0, departure_time=0)
    assert board.resolve_arrival(move) is True


# ---------- is_move_valid_on_board ----------

def test_is_move_valid_on_board_delegates_to_the_piece_rules(make_board):
    board = make_board("wR . .")
    rook = board.get_piece_at(0, 0)
    assert board.is_move_valid_on_board(rook, (0, 0), (0, 2)) is True


def test_is_move_valid_on_board_false_for_an_illegal_step(make_board):
    board = make_board(
        "wR . .",
        ". . .",
    )
    rook = board.get_piece_at(0, 0)
    assert board.is_move_valid_on_board(rook, (0, 0), (1, 2)) is False


# ---------- print_board ----------

def test_print_board_prints_one_line_per_row_space_separated(make_board, capsys):
    board = make_board("wR . .", ". bK .")
    board.print_board()
    printed = capsys.readouterr().out.strip().splitlines()
    assert printed == ["wR . .", ". bK ."]
