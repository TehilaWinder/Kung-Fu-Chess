def check_bloking(board, prev_place, new_place):
    r_prev, c_prev = prev_place
    r_new, c_new = new_place
    delta_row = r_new - r_prev
    delta_col = c_new - c_prev

    step_row = 0 if delta_row == 0 else (1 if delta_row > 0 else -1)
    step_col = 0 if delta_col == 0 else (1 if delta_col > 0 else -1)

    current_row, current_col = r_prev + step_row, c_prev + step_col

    while (current_row, current_col) != (r_new, c_new):
        if board[current_row][current_col] != ".":
            return True
        current_row += step_row
        current_col += step_col

    return False
