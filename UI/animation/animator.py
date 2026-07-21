from UI.assets.sprite_loader import load_sprite
from UI.assets.piece_config import get_piece_config


def _compute_frame(piece_code, state, since, clock):
    config = get_piece_config(piece_code, state)
    elapsed = max(0, clock - since)
    frame_index = int(elapsed * config["frames_per_sec"] / 1000)
    if config["is_loop"]:
        frame_index %= config["frame_count"]
    else:
        frame_index = min(frame_index, config["frame_count"] - 1)
    return frame_index + 1  # קבצי הספרייטים ממוספרים 1.png, 2.png, ...


class Animator:
    def render(self, piece_views, canvas, clock, offset_x=0):
        """מצייר את כל הכלים שנמסרו לו, בדיוק לפי המצב, המיקום, וזמן המשחק הנוכחי"""
        for pv in piece_views:
            frame = _compute_frame(pv.piece_code, pv.state, pv.since, clock)
            sprite = load_sprite(pv.piece_code, state=pv.state, frame=frame)
            sprite.draw_on(canvas, pv.x + offset_x, pv.y)
