def is_piece_moving(pending_moves, row, col):
    for move in pending_moves:
        if move["from_cell"] == (row, col) or move["to_cell"] == (row, col):
            return True
    return False