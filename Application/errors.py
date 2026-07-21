class BoardValidationError(Exception):
    """Base exception for invalid board input."""


class RowWidthMismatchError(BoardValidationError):
    def __init__(self):
        super().__init__("ERROR ROW_WIDTH_MISMATCH")


class UnknownTokenError(BoardValidationError):
    def __init__(self):
        super().__init__("ERROR UNKNOWN_TOKEN")
