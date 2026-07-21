# -*- coding: utf-8 -*-
"""
טסטים ליחידה Entities/position.py - מחלקת Position בלבד.
כל טסט בודק התנהגות אחת ומדויקת (unit test אמיתי, בלי תלות בלוח/משחק).
"""
from Entities.position import Position


def test_equal_positions_with_same_row_and_col_are_equal():
    assert Position(2, 3) == Position(2, 3)


def test_positions_with_different_row_are_not_equal():
    assert Position(2, 3) != Position(5, 3)


def test_positions_with_different_col_are_not_equal():
    assert Position(2, 3) != Position(2, 9)


def test_unpacking_position_yields_row_then_col():
    row, col = Position(4, 7)
    assert (row, col) == (4, 7)


def test_equal_positions_have_equal_hash():
    # דרישה הכרחית ב-Python: אובייקטים שווים (==) חייבים hash זהה,
    # אחרת אי אפשר לשים אותם ב-set/dict בביטחון.
    assert hash(Position(1, 1)) == hash(Position(1, 1))


def test_position_can_be_used_as_dict_key():
    lookup = {Position(0, 0): "start"}
    assert lookup[Position(0, 0)] == "start"


def test_str_shows_row_and_col():
    assert str(Position(3, 4)) == "(3, 4)"
