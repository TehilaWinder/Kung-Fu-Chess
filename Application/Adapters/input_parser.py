import sys
import config as cg


class InputParser:
  

    def read_from_stdin(self):
        raw = sys.stdin.read()
        return self.parse(raw)

    def parse(self, text):
       
        lines = text.splitlines()

        board_lines = []
        command_lines = []
        is_board_section = False

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line == cg.BOARD:
                is_board_section = True
                continue

            if line == cg.COMMANDS:
                is_board_section = False
                continue

            if is_board_section:
                board_lines.append(line.split())
            else:
                command_lines.append(line)

        return board_lines, command_lines
