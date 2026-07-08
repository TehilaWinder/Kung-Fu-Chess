from iterate4 import check_bloking

def check_valid_step(board,prev_place,new_place):
    r_prev, c_prev = prev_place
    r_new, c_new = new_place
    piece=board[r_prev][c_prev][1]
    delta_row = abs(r_new - r_prev)
    delta_col = abs(c_new - c_prev)
    is_legal = False

    if piece == 'K':
        if delta_row <= 1 and delta_col <= 1 and (delta_row > 0 or delta_col > 0):
            is_legal = True
    elif piece == 'R':
        if delta_row == 0 or delta_col == 0:
            if not check_bloking(board, prev_place, new_place):
                is_legal = True
    elif piece == 'B':
        if delta_row == delta_col :
            if not check_bloking(board, prev_place, new_place):
                is_legal = True
    elif piece == 'Q':
        if delta_row == 0 or delta_col == 0 or delta_row == delta_col:
            if not check_bloking(board, prev_place, new_place):
                is_legal = True
    elif piece == 'N':
        if (delta_row == 2 and delta_col == 1) or (delta_row == 1 and delta_col == 2):
            is_legal = True
    elif piece == 'P':        
        if delta_col == 0 and  delta_row==1:
            if board[r_new][c_new] == '.' :
                is_legal = True
        elif delta_col == 1 and delta_row == 1:
            target_piece = board[r_new][c_new]
            if target_piece != '.' and target_piece[0] != piece[0]:
                is_legal = True
    return is_legal
    