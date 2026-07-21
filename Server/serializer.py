"""Converts Chess state to JSON-safe dict using protocol field names."""
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from Server.protocol import (
    TYPE_STATE, FIELD_TYPE, FIELD_CLOCK, FIELD_PIECES,
    FIELD_SCORES, FIELD_LOG, FIELD_OVER, FIELD_WINNER,
    FIELD_COLOR, FIELD_ROW, FIELD_COL
)


def _serialize_move(move):
    return {
        "from_cell": list(move.from_cell),
        "to_cell": list(move.to_cell),
        "arrival_time": move.arrival_time,
        "departure_time": move.departure_time,
        "path": [
            {FIELD_ROW: seg.row, FIELD_COL: seg.col, "arrival_time": seg.arrival_time}
            for seg in move.path
        ],
    }


def _serialize_piece(piece_position):
    return {
        "piece_code": piece_position.piece_code,
        "state": piece_position.state,
        "since": piece_position.since,
        FIELD_ROW: piece_position.row,
        FIELD_COL: piece_position.col,
        "move": _serialize_move(piece_position.move) if piece_position.move else None,
    }


def snapshot_to_dict(game, move_log) -> dict:
    positions = game.scheduler.get_visual_state(game.board)
    colors = list(game.scores.keys())

    if move_log is None:
        log_by_color = {color: [] for color in colors}
    else:
        log_by_color = {color: move_log.entries_for(color) for color in colors}

    return {
        FIELD_TYPE: TYPE_STATE,
        FIELD_CLOCK: game.scheduler.game_clock,
        FIELD_PIECES: [_serialize_piece(pp) for pp in positions],
        FIELD_SCORES: {color: score.score for color, score in game.scores.items()},
        FIELD_LOG: log_by_color,
        FIELD_OVER: game.is_game_over,
        FIELD_WINNER: game.get_winner() if game.is_game_over else None,
    }


if __name__ == "__main__":
    import json

    sys.path.insert(0, os.path.join(_PROJECT_ROOT, "Day1"))

    from Service.chess_game import Chess
    from UI.config.board_setup import START_BOARD

    game = Chess(START_BOARD)
    snapshot = snapshot_to_dict(game, None)
    print(json.dumps(snapshot, indent=2))
