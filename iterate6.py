import iterate2 as utils
def update_board(game_clock, board, pending_moves):
    # 1. למיין את התנועות לפי זמן ההגעה (כדי לטפל במי שהגיע קודם)
    pending_moves.sort(key=lambda x: x["arrival_time"])
    
    remaining_moves = []
    
    for move in pending_moves:
        # אם זמן ההגעה של המהלך עדיין לא הגיע, הוא נשאר בתור לעתיד
        if move["arrival_time"] > game_clock:
            remaining_moves.append(move)
            continue
            
        # הגענו לזמן ההגעה! נבדוק מה קורה במשבצת היעד
        r_to, c_to = move["to_cell"]
        r_from, c_from = move["from_cell"]
        piece = move["piece"]
        existing_color = utils.get_piece_color(board, r_to, c_to)
        
        if utils.is_empty(board, r_to, c_to) or existing_color != piece[0]:
            # משבצת ריקה - נחיתה מוצלחת
            utils.set_piece_at(board, r_to, c_to, piece)
            if board[r_from][c_from] == piece:
                utils.set_piece_at(board, r_from, c_from, utils.EMPTY_CELL)
            
        else:
            pass

    return remaining_moves
