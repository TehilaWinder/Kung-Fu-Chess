class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __iter__(self):
        # מאפשר unpacking כמו טופל: row, col = position
        yield self.row
        yield self.col

    def __str__(self):
        return f"({self.row}, {self.col})"
