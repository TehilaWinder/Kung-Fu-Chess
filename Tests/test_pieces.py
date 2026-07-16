# -*- coding: utf-8 -*-
"""
טסטים ליחידה Entities/pieces.py - חוקי התנועה של כל סוג כלי (is_valid_step),
בלוק דרך (check_blocking), הכתרה (promote) והתנהגויות בסיס (Piece).

כל טסט משתמש ב-fixture בשם make_board (מוגדר ב-conftest.py) כדי לבנות
לוח אמיתי מתוך שורות ASCII, ובודק ישירות את piece.is_valid_step(...) -
בלי לעבור דרך המשחק כולו.
"""
import config as cg
from Entities.pieces import King, Rook, Bishop, Queen, Knight, Pawn, TYPE_TO_CLASS


# ---------- Piece (base behaviour, via a concrete subclass) ----------

def test_str_shows_color_and_type():
    assert str(Rook("w", "R")) == "wR"


def test_is_king_true_for_king():
    assert King("w", "K").is_king() is True


def test_is_king_false_for_non_king():
    assert Rook("w", "R").is_king() is False


def test_can_capture_enemy_piece():
    assert Rook("w", "R").can_capture(Rook("b", "R")) is True


def test_cannot_capture_own_color_piece():
    assert Rook("w", "R").can_capture(Rook("w", "R")) is False


def test_default_promote_returns_the_same_piece(make_board):
    board = make_board("wR . .")
    rook = board.get_piece_at(0, 0)
    assert rook.promote(board, (0, 2)) is rook


def test_type_to_class_maps_every_letter_to_its_class():
    assert TYPE_TO_CLASS == {
        'K': King, 'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight, 'P': Pawn,
    }


# ---------- King ----------

def test_king_can_step_one_square_in_any_direction(make_board):
    board = make_board(
        ". . .",
        ". wK .",
        ". . .",
    )
    king = board.get_piece_at(1, 1)
    for target in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]:
        assert king.is_valid_step(board, (1, 1), target) is True


def test_king_cannot_stay_in_place(make_board):
    board = make_board(". wK .")
    king = board.get_piece_at(0, 1)
    assert king.is_valid_step(board, (0, 1), (0, 1)) is False


def test_king_cannot_move_two_squares(make_board):
    board = make_board(". . wK . .")
    king = board.get_piece_at(0, 2)
    assert king.is_valid_step(board, (0, 2), (0, 0)) is False


# ---------- Rook ----------

def test_rook_can_move_horizontally_on_a_clear_path(make_board):
    board = make_board("wR . . .")
    rook = board.get_piece_at(0, 0)
    assert rook.is_valid_step(board, (0, 0), (0, 3)) is True


def test_rook_can_move_vertically_on_a_clear_path(make_board):
    board = make_board(
        "wR . .",
        ". . .",
        ". . .",
    )
    rook = board.get_piece_at(0, 0)
    assert rook.is_valid_step(board, (0, 0), (2, 0)) is True


def test_rook_cannot_jump_over_a_piece_in_its_path(make_board):
    board = make_board("wR bR . .")
    rook = board.get_piece_at(0, 0)
    assert rook.is_valid_step(board, (0, 0), (0, 3)) is False


def test_rook_cannot_move_diagonally(make_board):
    board = make_board(
        "wR . .",
        ". . .",
        ". . .",
    )
    rook = board.get_piece_at(0, 0)
    assert rook.is_valid_step(board, (0, 0), (2, 2)) is False


# ---------- Bishop ----------

def test_bishop_can_move_diagonally_on_a_clear_path(make_board):
    board = make_board(
        "wB . .",
        ". . .",
        ". . .",
    )
    bishop = board.get_piece_at(0, 0)
    assert bishop.is_valid_step(board, (0, 0), (2, 2)) is True


def test_bishop_cannot_jump_over_a_piece_on_the_diagonal(make_board):
    board = make_board(
        "wB . .",
        ". bR .",
        ". . .",
    )
    bishop = board.get_piece_at(0, 0)
    assert bishop.is_valid_step(board, (0, 0), (2, 2)) is False


def test_bishop_cannot_move_in_a_straight_line(make_board):
    board = make_board("wB . .")
    bishop = board.get_piece_at(0, 0)
    assert bishop.is_valid_step(board, (0, 0), (0, 2)) is False


# ---------- Queen ----------

def test_queen_can_move_horizontally(make_board):
    board = make_board("wQ . .")
    queen = board.get_piece_at(0, 0)
    assert queen.is_valid_step(board, (0, 0), (0, 2)) is True


def test_queen_can_move_diagonally(make_board):
    board = make_board(
        "wQ . .",
        ". . .",
        ". . .",
    )
    queen = board.get_piece_at(0, 0)
    assert queen.is_valid_step(board, (0, 0), (2, 2)) is True


def test_queen_cannot_jump_over_a_blocking_piece(make_board):
    board = make_board("wQ bR . .")
    queen = board.get_piece_at(0, 0)
    assert queen.is_valid_step(board, (0, 0), (0, 3)) is False


def test_queen_cannot_move_like_a_knight(make_board):
    board = make_board(
        "wQ . .",
        ". . .",
        ". . .",
    )
    queen = board.get_piece_at(0, 0)
    assert queen.is_valid_step(board, (0, 0), (2, 1)) is False


# ---------- Knight ----------

def test_knight_can_move_in_an_l_shape(make_board):
    board = make_board(
        "wN . .",
        ". . .",
        ". . .",
    )
    knight = board.get_piece_at(0, 0)
    assert knight.is_valid_step(board, (0, 0), (2, 1)) is True


def test_knight_can_jump_over_pieces_in_between(make_board):
    board = make_board(
        "wN bR .",
        "bR bR .",
        ". . .",
    )
    knight = board.get_piece_at(0, 0)
    assert knight.is_valid_step(board, (0, 0), (2, 1)) is True


def test_knight_cannot_move_in_a_straight_line(make_board):
    board = make_board("wN . .")
    knight = board.get_piece_at(0, 0)
    assert knight.is_valid_step(board, (0, 0), (0, 2)) is False


# ---------- Pawn ----------

def test_white_pawn_can_step_one_square_forward_into_empty_cell(make_board):
    board = make_board(
        ". . .",
        "wP . .",
        ". . .",
    )
    pawn = board.get_piece_at(1, 0)
    assert pawn.is_valid_step(board, (1, 0), (0, 0)) is True


def test_white_pawn_can_step_two_squares_forward_from_its_start_row(make_board):
    board = make_board(
        ". . .",
        ". . .",
        "wP . .",
    )
    pawn = board.get_piece_at(2, 0)
    assert pawn.is_valid_step(board, (2, 0), (0, 0)) is True


def test_white_pawn_cannot_step_two_squares_forward_outside_its_start_row(make_board):
    # לוח בגובה 4: שורת ההתחלה של הלבן היא השורה התחתונה (3), לא שורה 2
    board = make_board(
        ". . .",
        ". . .",
        "wP . .",
        ". . .",
    )
    pawn = board.get_piece_at(2, 0)
    assert pawn.is_valid_step(board, (2, 0), (0, 0)) is False


def test_pawn_cannot_move_forward_into_an_occupied_cell(make_board):
    board = make_board(
        "bR . .",
        "wP . .",
        ". . .",
    )
    pawn = board.get_piece_at(1, 0)
    assert pawn.is_valid_step(board, (1, 0), (0, 0)) is False


def test_white_pawn_double_step_is_blocked_by_a_piece_in_between(make_board):
    board = make_board(
        "bR . .",
        ". . .",
        "wP . .",
    )
    pawn = board.get_piece_at(2, 0)
    assert pawn.is_valid_step(board, (2, 0), (0, 0)) is False


def test_pawn_can_capture_diagonally_when_an_enemy_is_there(make_board):
    board = make_board(
        ". bR .",
        "wP . .",
        ". . .",
    )
    pawn = board.get_piece_at(1, 0)
    assert pawn.is_valid_step(board, (1, 0), (0, 1)) is True


def test_pawn_cannot_capture_diagonally_into_an_empty_cell(make_board):
    board = make_board(
        ". . .",
        "wP . .",
        ". . .",
    )
    pawn = board.get_piece_at(1, 0)
    assert pawn.is_valid_step(board, (1, 0), (0, 1)) is False


def test_pawn_cannot_capture_diagonally_a_piece_of_its_own_color(make_board):
    board = make_board(
        ". . .",
        "wP wR .",
        ". . .",
    )
    pawn = board.get_piece_at(1, 0)
    assert pawn.is_valid_step(board, (1, 0), (0, 1)) is False


def test_black_pawn_moves_downward(make_board):
    board = make_board(
        "bP . .",
        ". . .",
        ". . .",
    )
    pawn = board.get_piece_at(0, 0)
    assert pawn.is_valid_step(board, (0, 0), (1, 0)) is True


def test_pawn_promotes_to_queen_on_the_last_row(make_board):
    board = make_board(
        ". . .",
        "wP . .",
    )
    pawn = board.get_piece_at(1, 0)
    promoted = pawn.promote(board, (0, 0))
    assert isinstance(promoted, Queen)
    assert promoted.color == cg.COLOR_WHITE


def test_pawn_does_not_promote_before_the_last_row(make_board):
    board = make_board(
        ". . .",
        ". . .",
        "wP . .",
    )
    pawn = board.get_piece_at(2, 0)
    assert pawn.promote(board, (1, 0)) is pawn
