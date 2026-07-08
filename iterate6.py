
def update_board(game_clock, board,pending_moves):
    still_pending = []
    
    for move in pending_moves:
        if game_clock >= move["arrival_time"]:
            r_from, c_from = move["from_cell"]
            r_to, c_to = move["to_cell"]
            
            board[r_to][c_to] = move["piece"]
            if board[r_from][c_from] == move["piece"]:
                board[r_from][c_from] = "."
        else:
            still_pending.append(move)
            
    return still_pending
