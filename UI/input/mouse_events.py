import cv2

from UI.input.click_adapter import pixel_to_cell


def make_mouse_handler(game, cell_size, offset_x=0):
    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            row, col = pixel_to_cell(x, y, cell_size, offset_x)
            game.handle_click(row, col)

        if event==cv2.EVENT_LBUTTONDBLCLK:
            row, col = pixel_to_cell(x, y, cell_size, offset_x)
            game.handle_jump(row,col)
    return on_mouse
