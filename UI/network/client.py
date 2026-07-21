"""NetworkClient: bridges asyncio WebSocket and the synchronous OpenCV loop."""
import asyncio
import json
import queue
import threading
import websockets

from Server.protocol import *


class NetworkClient:
    def __init__(self, username: str, uri: str = "ws://localhost:8765"):
        self._username = username
        self._uri = uri
        self._outgoing = queue.Queue()       # click/jump → server
        self._latest_state = None            # last snapshot from server
        self._lock = threading.Lock()
        self._color = None                   # "w" or "b", set after welcome
        self._connected = threading.Event()  # set when color is assigned
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        """Start background thread and block until color is assigned."""
        self._thread.start()
        self._connected.wait()  # block main thread until welcome received

    def send_click(self, row: int, col: int):
        self._outgoing.put({FIELD_TYPE: TYPE_CLICK, FIELD_ROW: row, FIELD_COL: col})

    def send_jump(self, row: int, col: int):
        self._outgoing.put({FIELD_TYPE: TYPE_JUMP, FIELD_ROW: row, FIELD_COL: col})

    def get_latest_state(self):
        with self._lock:
            return self._latest_state

    @property
    def color(self):
        return self._color

    def _run(self):
        asyncio.run(self._async_loop())

    async def _async_loop(self):
        async with websockets.connect(self._uri) as ws:
            # send login
            await ws.send(json.dumps({FIELD_TYPE: TYPE_LOGIN, "username": self._username}))

            # wait for welcome or error
            raw = await ws.recv()
            msg = json.loads(raw)

            if msg[FIELD_TYPE] == TYPE_ERROR:
                print(f"Server error: {msg[FIELD_MESSAGE]}")
                self._connected.set()  # unblock main thread
                return

            self._color = msg[FIELD_COLOR]
            self._connected.set()  # unblock main thread

            # run sender and receiver concurrently
            await asyncio.gather(
                self._sender(ws),
                self._receiver(ws)
            )

    async def _receiver(self, ws):
        async for raw in ws:
            msg = json.loads(raw)
            if msg.get(FIELD_TYPE) == TYPE_STATE:
                with self._lock:
                    self._latest_state = msg

    async def _sender(self, ws):
        loop = asyncio.get_event_loop()
        while True:
            try:
                msg = await loop.run_in_executor(
                    None,
                    lambda: self._outgoing.get(timeout=0.05)
                )
                await ws.send(json.dumps(msg))
            except queue.Empty:
                pass
