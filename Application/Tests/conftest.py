# -*- coding: utf-8 -*-
"""
כלי עזר (fixtures) המשותפים לכל קבצי הטסטים בתיקייה הזו.
pytest טוען את הקובץ הזה אוטומטית - אין צורך לייבא אותו בשום מקום.
"""
import pytest

import config as cg
from Entities.board import Board
from Entities.score import Score
from Service.chess_game import Chess


def parse_board(*rows):
    """
    הופכת שורות קריאות בפורמט "wK . ." לפורמט שה-Board מצפה לו
    (רשימת רשימות של טוקנים - בדיוק כמו שה-InputParser מייצר).

    שימוש בטסט:
        board_lines = parse_board(
            ". . .",
            "wK bR .",
            ". . .",
        )
    """
    return [row.split() for row in rows]


@pytest.fixture
def make_board():
    """Fixture שמחזירה פונקציה לבניית Board תקין מתוך שורות ASCII."""

    def _make(*rows):
        board = Board()
        assert board.load_and_validate(parse_board(*rows)), "בניית הלוח נכשלה - בדקי את תווי הקלט"
        return board

    return _make


@pytest.fixture
def make_scores():
    """Fixture שמחזירה מילון scores טרי ({צבע: Score}) לטסטים על Scheduler."""

    def _make():
        return {
            cg.COLOR_WHITE: Score(cg.COLOR_WHITE),
            cg.COLOR_BLACK: Score(cg.COLOR_BLACK),
        }

    return _make


@pytest.fixture
def make_game():
    """Fixture שמחזירה פונקציה לבניית משחק Chess תקין מתוך שורות ASCII."""

    def _make(*rows):
        game = Chess(parse_board(*rows))
        assert game.is_valid_setup, "בניית המשחק נכשלה - בדקי את תווי הקלט"
        return game

    return _make
