from dataclasses import dataclass


@dataclass
class Event:
    name: str
    data: object = None


# Event names
MOVE_COMPLETED = "MOVE_COMPLETED"
GAME_OVER      = "GAME_OVER"
GAME_STARTED   = "GAME_STARTED"
