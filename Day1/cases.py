# -*- coding: utf-8 -*-
"""
מאגר טסטים בפורמט הקלט הגולמי (בדיוק כמו ש-VPL/main.py מצפים לקבל בסטדין).
כל טסט הוא: (name, input_text, expected_output)

הטסטים מבוססים על אותם תרחישים שנמצאים ב-Tests/test_chess_game.py,
רק מתורגמים בחזרה לפורמט טקסט גולמי (Board: / Commands:) כדי שאפשר
להריץ אותם ישירות מול Adapters/main.py בדיוק כמו ש-VPL עושה.
"""

TEST_CASES = [
    (
        "jump_lands_same_square",
        """Board:
. . .
. wK .
. . .
Commands:
jump 150 150
wait 1000
print board
""",
        ". . .\n. wK .\n. . .",
    ),
    (
        "jump_catches_incoming_enemy",
        """Board:
. . .
wK bR .
. . .
Commands:
jump 50 150
click 150 150
click 50 150
wait 1000
print board
""",
        ". . .\nwK . .\n. . .",
    ),
    (
        "late_jump_does_not_save_piece",
        """Board:
. . .
wK bR .
. . .
Commands:
click 150 150
click 50 150
wait 1000
jump 50 150
print board
""",
        ". . .\nbR . .\n. . .",
    ),
    (
        "enemy_arrives_after_landing_and_captures_normally",
        """Board:
. . . .
wK . . bR
. . . .
Commands:
jump 50 150
wait 1000
click 350 150
click 50 150
wait 3000
print board
""",
        ". . . .\nbR . . .\n. . . .",
    ),
    (
        "cannot_jump_while_piece_is_moving",
        """Board:
wR . .
Commands:
click 50 50
click 250 50
wait 500
jump 50 50
wait 1500
print board
""",
        ". . wR",
    ),
    (
        "airborne_piece_cannot_capture_same_color",
        """Board:
. . .
wK wR .
. . .
Commands:
jump 50 150
click 150 150
click 50 150
wait 1000
print board
""",
        ". . .\nwK wR .\n. . .",
    ),
]
