# ==========================================
# קבועים (Constants) 
# ==========================================
CELL_SIZE = 100
TIME_PER_CELL = 1000
EMPTY_CELL = "."
PRINT="print"
WAIT="wait"
CLICK="click"

# ==========================================
# פונקציות עזר לגישה ללוח (הכמסה והכנה לשינוי עתידי)
# ==========================================

def get_piece_at(board, row, col):
    
    return board[row][col]

def set_piece_at(board, row, col, piece):
    
    board[row][col] = piece

def is_empty(board, row, col):
   
    return get_piece_at(board, row, col) == EMPTY_CELL

def get_piece_color(board, row, col):
    
    if is_empty(board, row, col):
        return None
    piece = get_piece_at(board, row, col)
    return piece[0]

def get_piece_type(board, row, col):
    if is_empty(board, row, col):
        return None
    piece = get_piece_at(board, row, col)
    return piece[1]

def calculate_travel_time(from_cell, to_cell):
    r_from, c_from = from_cell
    r_to, c_to = to_cell
    delta_row = abs(r_to - r_from)
    delta_col = abs(c_to - c_from)
    return max(delta_row, delta_col) * TIME_PER_CELL

def append_move(pending_moves, from_cell, to_cell, piece, arrival_time):
    pending_moves.append({
        "from_cell": from_cell,
        "to_cell": to_cell,
        "piece": piece,
        "arrival_time": arrival_time
    })
def get_cmd(input_string):
    parts = input_string.split()
    if not parts:
        return None, []
    cmd = parts[0]
    args = parts[1:]
    return cmd, args
def get_x_y(part):
    x = int(part[0])
    y = int(part[1])
    return x, y
def get_row_col_from_click(part):
    x, y = get_x_y(part)
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col
