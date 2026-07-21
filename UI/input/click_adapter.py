def pixel_to_cell(x, y, cell_size, offset_x=0):
    row = y // cell_size
    col = (x - offset_x) // cell_size
    return row, col