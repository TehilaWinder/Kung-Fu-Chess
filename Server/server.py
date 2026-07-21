"""Entry point. Owns Chess, accepts WS connections, runs tick loop."""
import asyncio
import json
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_APPLICATION_ROOT = os.path.join(_PROJECT_ROOT, "Application")
if _APPLICATION_ROOT not in sys.path:
    sys.path.insert(0, _APPLICATION_ROOT)

import websockets.asyncio.server

from Server.protocol import *
from Server.serializer import snapshot_to_dict
from UI.view.move_log import MoveLog
from UI.config.board_setup import START_BOARD

import config as cg
from Service.chess_game import Chess
from Application.Infrastructure.event_bus import InMemoryEventBus
from Application.Infrastructure.events import MOVE_COMPLETED

TICK_MS = 30

bus = InMemoryEventBus()
game = Chess(START_BOARD, bus=bus)
move_log = MoveLog()
bus.subscribe(MOVE_COMPLETED, move_log.on_move_completed)

white_ws = None
black_ws = None
tick_task = None


async def broadcast(snapshot_dict):
    msg = json.dumps(snapshot_dict)
    for ws in (white_ws, black_ws):
        if ws is not None:
            await ws.send(msg)


async def tick_loop():
    while True:
        await asyncio.sleep(TICK_MS / 1000)
        game.advance_clock(TICK_MS)
        await broadcast(snapshot_to_dict(game, move_log))


async def handle_client(websocket, color):
    async for raw in websocket:
        msg = json.loads(raw)
        msg_type = msg.get(FIELD_TYPE)

        if msg_type == TYPE_LOGIN:
            continue
        elif msg_type == TYPE_CLICK:
            game.handle_click(msg[FIELD_ROW], msg[FIELD_COL], color=color)
        elif msg_type == TYPE_JUMP:
            game.handle_jump(msg[FIELD_ROW], msg[FIELD_COL], color=color)
        else:
            continue

        await broadcast(snapshot_to_dict(game, move_log))


async def on_connect(websocket):
    global white_ws, black_ws, tick_task

    if white_ws is None:
        color = cg.COLOR_WHITE
        white_ws = websocket
    elif black_ws is None:
        color = cg.COLOR_BLACK
        black_ws = websocket
    else:
        await websocket.send(json.dumps({FIELD_TYPE: TYPE_ERROR, FIELD_MESSAGE: "game full"}))
        await websocket.close()
        return

    await websocket.send(json.dumps({FIELD_TYPE: TYPE_WELCOME, FIELD_COLOR: color}))

    if white_ws is not None and black_ws is not None and tick_task is None:
        tick_task = asyncio.create_task(tick_loop())

    try:
        await handle_client(websocket, color)
    finally:
        if websocket is white_ws:
            white_ws = None
        elif websocket is black_ws:
            black_ws = None


async def main():
    async with websockets.asyncio.server.serve(on_connect, "localhost", 8765):
        print("Server listening on ws://localhost:8765")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
