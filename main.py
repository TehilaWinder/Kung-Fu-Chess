from iterate1 import get_board_and_commands, print_board
from iterate3 import check_valid_step
from iterate6 import update_board
from iterate7 import is_piece_moving
from iterate8 import is_cell_in_any_path
import iterate2 as utils

board, commands = get_board_and_commands()

if board is None or commands is None:
    exit()
    
game_clock = 0
selected_piece = None
pending_moves = []
HEIGHT = len(board)
WIDTH = len(board[0]) if HEIGHT > 0 else 0
for command in commands:
    
    cmd, part = utils.get_cmd(command)
    if cmd == utils.PRINT:
        pending_moves = update_board(game_clock, board, pending_moves)
        print_board(board)
    
    if cmd == utils.CLICK:
        pending_moves = update_board(game_clock, board, pending_moves)
        
        row, col = utils.get_row_col_from_click(part)
        if row < 0 or row >= HEIGHT or col < 0 or col >= WIDTH:
            continue
        
        if is_piece_moving(pending_moves, row, col) or is_cell_in_any_path(pending_moves, row, col):
            selected_piece = None  # נבטל את הבחירה אם המשבצת בתנועה
            continue
        
        if selected_piece is None:
            # אם המשבצת ריקה, אין מה לבחור - נמשיך הלאה
            if utils.is_empty(board, row, col):
                continue
            # אם יש שם כלי - נשמור אותו ככלי הנבחר
            selected_piece = (row, col)
            continue
            
        
        else:
            # בדיקת חוקיות התנועה (האם הכלי מסוגל להגיע לשם לוגית)
            if not check_valid_step(board, selected_piece, (row, col)):
                selected_piece = None  # נבטל את הבחירה אם המהלך לא חוקי
                continue
            
            # שליפת נתוני כלי המקור
            r_src, c_src = selected_piece
            piece = utils.get_piece_at(board, r_src, c_src)
            
            # חישוב זמנים
            travel_time = utils.calculate_travel_time(selected_piece, (row, col))
            arrival_time = game_clock + travel_time
             
            # רישום התנועה בתור התנועות העתידיות
            utils.append_move(pending_moves, selected_piece, (row, col), piece, arrival_time)
            
            # איפוס הבחירה לקראת המהלך הבא
            selected_piece = None
        
    if cmd == utils.WAIT:
        game_clock += int(part[0])
