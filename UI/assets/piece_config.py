import json
from pathlib import Path

from UI.config.ui_config import PIECES_DIR

_cache = {}


def get_piece_config(piece_code, state):
    key = (piece_code, state)
    if key not in _cache:
        state_dir = Path(PIECES_DIR) / piece_code / "states" / state
        with open(state_dir / "config.json", encoding="utf-8") as f:
            raw = json.load(f)

        physics = raw["physics"]
        graphics = raw["graphics"]

        _cache[key] = {
            "frames_per_sec": graphics["frames_per_sec"],
            "is_loop": graphics["is_loop"],
            "speed_m_per_sec": physics["speed_m_per_sec"],
            "next_state_when_finished": physics["next_state_when_finished"],
            "frame_count": len(list((state_dir / "sprites").glob("*.png"))),
        }
    return _cache[key]
