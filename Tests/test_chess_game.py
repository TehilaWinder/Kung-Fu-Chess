import pytest
import config as cg
from Service.chess_game import Chess

# =====================================================================
# הגדרת נתוני הטסטים של המרצה (העתק-הדבק מדויק של הקלטים והפלטים)
# =====================================================================
TEST_CASES = [
    # טסט 1: בדיקת פקודת jump ו-wait בסיסית
    (
        ["wK . .", ".  . .", ".  . ."],  # לוח התחלתי (שורות)
        [("jump", 150, 150), ("wait", 1000), ("print", "board")],  # פקודות מתורגמות
        ". .\n. wK .\n. ."  # פלט צפוי (נרמל למחרוזת אחת)
    ),
    
    # טסט 2: כלי באוויר אוכל אויב שמגיע
    (
        [". . .", "wK bR .", ". . ."],
        [("jump", 50, 150), ("click", 150, 150), ("click", 50, 150), ("wait", 1000), ("print", "board")],
        ". . .\nwK . .\n. . ."
    ),
    
    # טסט 3: jump מאוחר מדי לא מציל את הכלי
    (
        [". . .", "wK bR .", ". . ."],
        [("click", 150, 150), ("click", 50, 150), ("wait", 1000), ("jump", 50, 150), ("print", "board")],
        ". . .\nbR . .\n. . ."
    ),
    
    # טסט 4: אויב מגיע אחרי נחיתה ואוכל רגיל
    (
        [". . . .", "wK . . bR", ". . . ."],
        [("jump", 50, 150), ("wait", 1000), ("click", 350, 150), ("click", 50, 150), ("wait", 3000), ("print", "board")],
        ". . . .\nbR . . .\n. . . ."
    ),
    
    # טסט 5: אי אפשר לעשות jump בזמן תנועה
    (
        ["wR . ."],
        [("click", 50, 50), ("click", 250, 50), ("wait", 500), ("jump", 50, 50), ("wait", 1500), ("print", "board")],
        ". . wR"
    ),
    
    # טסט 6: כלי באוויר יכול לאכול רק אויב (ולא כלי מאותו צבע)
    (
        [". . .", "wK wR .", ". . ."],
        [("jump", 50, 150), ("click", 150, 150), ("click", 50, 150), ("wait", 1000), ("print", "board")],
        ". . .\nwK wR .\n. . ."
    )
]

# =====================================================================
# פונקציית הטסט האוטומטית - רצה בלולאה על כל המקרים מעל!
# =====================================================================
@pytest.mark.parametrize("board_lines, commands, expected_output", TEST_CASES)
def test_instructor_scenarios(board_lines, commands, expected_output, capsys):
    """
    פונקציה אחת שמריצה את הלולאה על כל הקלטים.
    capsys הוא כלי של pytest שתופס את כל ה-print שהקוד שלך מייצר.
    """
    # 1. אתחול המשחק דרך ה-Service
    game = Chess(board_lines)
    assert game.is_valid_setup is True
    
    # 2. לולאת הרצת הפקודות (מדמה בדיוק את ה-main שלך)
    for cmd_type, *args in commands:
        if cmd_type == "click":
            x, y = args
            row = y // cg.CELL_SIZE
            col = x // cg.CELL_SIZE
            game.handle_click(row, col)
            
        elif cmd_type == "wait":
            time_to_wait = args[0]
            game.advance_clock(time_to_wait)
            
        elif cmd_type == "jump":
            x, y = args
            row = y // cg.CELL_SIZE
            col = x // cg.CELL_SIZE
            # TODO: כאן תקראי לפונקציית ה-jump החדשה שלך בסרוויס!
            # game.handle_jump(row, col) 
            pass 
            
        elif cmd_type == "print" and args[0] == "board":
            game.print_game()

    # 3. תפיסת ה-Output שהתוכנית הדפיסה והשוואה לציפייה של המרצה
    captured = capsys.readouterr()
    actual_output = captured.out.strip()
    
    # ניקוי רווחים מיותרים בשורות כדי למנוע כישלון על רווח קטן בסוף שורה
    normalized_actual = "\n".join([line.strip() for line in actual_output.split("\n") if line.strip()])
    normalized_expected = "\n".join([line.strip() for line in expected_output.split("\n") if line.strip()])
    
    assert normalized_actual == normalized_expected