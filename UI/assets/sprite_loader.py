from UI.graphics.img import Img
from UI.config.ui_config import CELL_SIZE, PIECES_DIR

_cache = {}


def load_sprite(piece_code, state="idle", frame=1):
    key = (piece_code, state, frame)
    if key not in _cache:
        path = f"{PIECES_DIR}/{piece_code}/states/{state}/sprites/{frame}.png"
        _cache[key] = Img().read(path, size=(CELL_SIZE, CELL_SIZE), keep_aspect=True)
    return _cache[key]
