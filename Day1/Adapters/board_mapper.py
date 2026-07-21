import config as cg
class BoardMapper:
    
        def pixel_to_cell(self, x, y):
            
            row = y // cg.CELL_SIZE
            col = x // cg.CELL_SIZE
            return (row, col)
        