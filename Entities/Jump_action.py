class JumpAction:
    def __init__(self, piece, row, col, landing_time):
        self.piece = piece
        self.cell = (row, col)  
        self.landing_time = landing_time

    def is_expired(self, current_time):
        """האם זמן הקפיצה עבר?"""
        return current_time > self.landing_time

    def intercepts(self, move):
        """
        האם הקפיצה הזו מיירטת (חוסמת ואוכלת) את המהלך הנתון?
        קורה רק אם יעד המהלך הוא משבצת הקפיצה, והכלי הוא כלי אויב.
        """
        return self.cell == move.to_cell and self.piece.color != move.piece.color