import config as cg

class Move:
    def __init__(self, from_cell, to_cell, piece, arrival_time):
        self.from_cell = from_cell       # טופל (row, col)
        self.to_cell = to_cell           # טופל (row, col)
        self.piece = piece               # אובייקט הכלים (Piece)
        self.arrival_time = arrival_time # זמן הגעה מוחלט בשעון

    def is_cell_in_path(self, r, c):
       
        r_src, c_src = self.from_cell
        r_dst, c_dst = self.to_cell
        
        if (r, c) == (r_src, c_src) or (r, c) == (r_dst, c_dst):
            return True
            
        # בדיקה אם (r,c) בטווח הכללי ובמסלול ישר/אלכסוני
        if min(r_src, r_dst) <= r <= max(r_src, r_dst) and min(c_src, c_dst) <= c <= max(c_src, c_dst):
            if r_src == r_dst == r: return True      # אופקי
            if c_src == c_dst == c: return True      # אנכי
            if abs(r - r_src) == abs(c - c_src): return True  # אלכסוני
            
        return False
    
    def starts_from(self, row, col):
        return self.from_cell == (row, col)

    def is_due(self, clock):
        return self.arrival_time <= clock