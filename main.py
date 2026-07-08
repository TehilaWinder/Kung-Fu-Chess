from iterate1 import get_board_and_commands, print_board
from iterate3 import check_valid_step
from iterate6 import update_board
from iterate7 import is_piece_moving
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
        if pending_moves:          
            continue
        row, col = utils.get_row_col_from_click(part)
        if row < 0 or row >= HEIGHT or col < 0 or col >= WIDTH:
            continue
        if is_piece_moving(pending_moves, row, col):
            continue
        
        #תנועה למשבצת ריקה
        if utils.is_empty(board, row, col):
            #אם עדיין לא נבחר שום חייל
            if selected_piece is None:
                continue
            else:
                if not check_valid_step(board, selected_piece, (row, col)):
                    continue
                r, c = selected_piece
                piece = utils.get_piece_at(board, r, c)
                travel_time = utils.calculate_travel_time(selected_piece, (row, col))
                arrival_time = game_clock + travel_time
                utils.append_move(pending_moves, selected_piece, (row, col), piece, arrival_time)
                selected_piece = None
        #תנועה למצב אכילה
        else:
            if selected_piece is None:
                selected_piece = (row, col)
            else:
                if not check_valid_step(board, selected_piece, (row, col)):
                    continue
                r, c = selected_piece
                piece1 = utils.get_piece_at(board, r, c)
                piece2 = utils.get_piece_at(board, row, col)
                piece1_color = utils.get_piece_color(board, r, c)
                piece2_color = utils.get_piece_color(board, row, col)
                if piece1_color == piece2_color:
                    selected_piece = None
                    continue
                else:
                    r, c = selected_piece
                    piece = utils.get_piece_at(board, r, c)
                    travel_time = utils.calculate_travel_time(selected_piece, (row, col))
                    arrival_time = game_clock + travel_time
                    utils.append_move(pending_moves, selected_piece, (row, col), piece, arrival_time)
                    selected_piece = None
        
    if cmd == utils.WAIT:
        game_clock += int(part[0])
