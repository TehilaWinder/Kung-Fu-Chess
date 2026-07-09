import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config as cg
from Adapters.input_parser import InputParser
from Service.chess_game import Chess
from Adapters.board_mapper import BoardMapper

parser = InputParser()
board_lines, command_lines = parser.read_from_stdin()
mapper = BoardMapper()

game = Chess(board_lines)

if not game.is_valid_setup:
    exit()

for command in command_lines:
    parts = command.split()
    if not parts:
        continue

    cmd = parts[0]

    if cmd == cg.CMD_PRINT:
        game.print_game()

    elif cmd == cg.CMD_CLICK:
        game.update_board()
        row, col = mapper.pixel_to_cell(int(parts[1]), int(parts[2]))
        game.handle_click(row, col)

    elif cmd == cg.CMD_WAIT:
        game.advance_clock(int(parts[1]))
    elif cmd == cg.CMD_JUMP:
        row, col = mapper.pixel_to_cell(int(parts[1]), int(parts[2]))
        game.handle_jump(row, col)
