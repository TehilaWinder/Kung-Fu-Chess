# -*- coding: utf-8 -*-
"""
טסטים ליחידה Entities/move.py - מחלקת Move בלבד.
"""
from Entities.move import Move
from Entities.position import Position
from Entities.pieces import Rook


def make_move(from_rc, to_rc, arrival_time=1000, departure_time=0):
    piece = Rook("w", "R")
    return Move(Position(*from_rc), Position(*to_rc), piece, arrival_time, departure_time)


# ---------- is_cell_in_path ----------

def test_path_includes_the_source_cell():
    move = make_move((0, 0), (0, 3))
    assert move.is_cell_in_path(0, 0) is True


def test_path_includes_the_destination_cell():
    move = make_move((0, 0), (0, 3))
    assert move.is_cell_in_path(0, 3) is True


def test_horizontal_path_includes_cell_between_source_and_destination():
    move = make_move((0, 0), (0, 3))
    assert move.is_cell_in_path(0, 2) is True


def test_vertical_path_includes_cell_between_source_and_destination():
    move = make_move((0, 0), (3, 0))
    assert move.is_cell_in_path(2, 0) is True


def test_diagonal_path_includes_cell_between_source_and_destination():
    move = make_move((0, 0), (3, 3))
    assert move.is_cell_in_path(2, 2) is True


def test_cell_off_the_line_is_not_in_path():
    move = make_move((0, 0), (0, 3))
    assert move.is_cell_in_path(1, 1) is False


def test_cell_on_the_same_line_but_outside_the_segment_is_not_in_path():
    move = make_move((0, 1), (0, 3))
    assert move.is_cell_in_path(0, 5) is False


# ---------- starts_from ----------

def test_starts_from_true_for_the_source_cell():
    move = make_move((2, 4), (5, 4))
    assert move.starts_from(2, 4) is True


def test_starts_from_false_for_any_other_cell():
    move = make_move((2, 4), (5, 4))
    assert move.starts_from(5, 4) is False


# ---------- is_due ----------

def test_is_due_false_before_arrival_time():
    move = make_move((0, 0), (0, 1), arrival_time=1000)
    assert move.is_due(999) is False


def test_is_due_true_exactly_at_arrival_time():
    move = make_move((0, 0), (0, 1), arrival_time=1000)
    assert move.is_due(1000) is True


def test_is_due_true_after_arrival_time():
    move = make_move((0, 0), (0, 1), arrival_time=1000)
    assert move.is_due(1500) is True


# ---------- departure_time ----------

def test_departure_time_is_stored_as_given():
    move = make_move((0, 0), (0, 1), arrival_time=1000, departure_time=200)
    assert move.departure_time == 200
