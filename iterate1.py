def print_board(board):
    for row in board:
        print(' '.join(row))

def get_board_and_commands():
    import sys
    lines = sys.stdin.read().splitlines()


    board_lines = []
    comand_lines = []   
    is_board_section = False
    first_line=True
    has_error = False
    VALID_PIECES = {'K', 'Q', 'R', 'B', 'N', 'P'}

    for line in lines:
            line = line.strip()
            
            if not line:
                continue 
                
            if line == "Board:":
                is_board_section = True
                continue 
                
            if line == "Commands:":
                is_board_section = False
                continue 
                
            if is_board_section:
                
                if first_line:
                    len_line=len(line.split())
                    first_line=False
                elif len_line!=len(line.split()):
                    print("ERROR ROW_WIDTH_MISMATCH")
                    has_error=True

                for token in line.split():
                    if token == '.':
                        continue 
                
                    if len(token) != 2 or token[0] not in ('w', 'b') or token[1] not in VALID_PIECES:
                        print("ERROR UNKNOWN_TOKEN")
                        has_error = True
                        break
                    
                if has_error:
                    return (None,None)
                board_lines.append(line.split())
            else:
                comand_lines.append(line)

        
                
    return (board_lines, comand_lines)




                
                
    