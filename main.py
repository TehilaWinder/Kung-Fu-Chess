import config as cg
from input_parser import InputParser
from chess_game import Chess

parser = InputParser()
board_lines, command_lines = parser.read_from_stdin()

game = Chess(board_lines)

if not game.is_valid_setup:
    exit()

for command in command_lines:
    parts = command.split()
    if not parts:
        continue

    cmd = parts[0]

    if cmd == cg.CMD_PRINT:
        game.update_board()
        game.board.print_board()

    elif cmd == cg.CMD_CLICK:
        game.update_board()
        row = int(parts[2]) // cg.CELL_SIZE
        col = int(parts[1]) // cg.CELL_SIZE
        game.handle_click(row, col)

    elif cmd == cg.CMD_WAIT:
        game.advance_clock(int(parts[1]))
