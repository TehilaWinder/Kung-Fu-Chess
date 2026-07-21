import os
import sys
import time
import cv2

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "Application"))

from UI.input.mouse_events import make_mouse_handler
from UI.game_renderer import GameRenderer
from UI.view.move_log import MoveLog
from UI.config.ui_config import CELL_SIZE
from UI.config.board_setup import START_BOARD
from Service.chess_game import Chess
from Application.Infrastructure.event_bus import InMemoryEventBus
from Application.Infrastructure.events import MOVE_COMPLETED

bus = InMemoryEventBus()
game = Chess(START_BOARD, bus=bus)

move_log = MoveLog()
bus.subscribe(MOVE_COMPLETED, move_log.on_move_completed)

renderer = GameRenderer(game, move_log)

cv2.namedWindow("Game")
cv2.setMouseCallback("Game", make_mouse_handler(game, CELL_SIZE, renderer.board_offset_x))

last_time = time.time()
while True:
    now = time.time()
    game.advance_clock((now - last_time) * 1000)
    last_time = now

    frame = renderer.render()

    cv2.imshow("Game", frame.img)
    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()
