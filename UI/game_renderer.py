import config as cg
from UI.graphics.img import Img
from UI.animation.animator import Animator
from UI.view.move_position_adapter import MovePositionAdapter
from UI.view.piece_view import PieceView
from UI.config.ui_config import CELL_SIZE, BOARD_SIZE, SCORE_PANEL_WIDTH, PANEL_BG_COLOR

MOVE_LOG_FONT_SIZE = 0.45
MOVE_LOG_LINE_HEIGHT = 22
MOVE_LOG_TEXT_COLOR = (160, 160, 160)


class GameRenderer:
    def __init__(self, game, move_log):
        self.game = game
        self.move_log = move_log
        self.animator = Animator()
        self.move_position_adapter = MovePositionAdapter(CELL_SIZE)
        self.board_pixels = CELL_SIZE * BOARD_SIZE
        self.board_offset_x = SCORE_PANEL_WIDTH
        self.canvas_width = self.board_pixels + 2 * SCORE_PANEL_WIDTH
        self.background = Img().read("./board.png", size=(self.board_pixels, self.board_pixels))

    def render(self):
        frame = Img.blank(self.canvas_width, self.board_pixels, color=PANEL_BG_COLOR)
        self.background.draw_on(frame, self.board_offset_x, 0)

        self._draw_score_panel(frame, panel_x=0, color=cg.COLOR_WHITE, label="White", show_move_log=True)
        self._draw_score_panel(frame, panel_x=self.board_offset_x + self.board_pixels, color=cg.COLOR_BLACK, label="Black", show_move_log=True)

        clock = self.game.scheduler.game_clock
        positions = self.game.scheduler.get_visual_state(self.game.board)
        piece_views = self._to_piece_views(positions, clock)
        self.animator.render(piece_views, frame, clock, offset_x=self.board_offset_x)

        if self.game.is_game_over:
            self._draw_game_over(frame)

        return frame

    def _to_piece_views(self, positions, clock) -> list[PieceView]:
        """ממירה מיקומים לוגיים (PiecePosition) לפיקסלים - הפרט הזה שייך ל-UI בלבד."""
        piece_views = []
        for pos in positions:
            if pos.state == "move":
                x, y = self.move_position_adapter.get_pixel_position(pos.move, clock)
            else:
                x, y = pos.col * CELL_SIZE, pos.row * CELL_SIZE
            piece_views.append(PieceView(pos.piece_code, x, y, pos.state, pos.since))
        return piece_views

    def _draw_game_over(self, frame):
        frame.dim(0.55)

        winner_names = {cg.COLOR_WHITE: "White", cg.COLOR_BLACK: "Black"}
        winner = self.game.get_winner()
        text = f"{winner_names[winner]} WINS!" if winner else "GAME OVER"

        text_x = self.canvas_width // 2 - 20 * len(text) // 2
        text_y = self.board_pixels // 2
        frame.put_text(text, text_x, text_y, font_size=1.6, color=(255, 255, 255), thickness=4)

    def _draw_score_panel(self, frame, panel_x, color, label, show_move_log=False):
        box_w, box_h = SCORE_PANEL_WIDTH - 40, 160
        box_x = panel_x + 20
        box_y = self.board_pixels // 2 - box_h // 2

        frame.draw_rect(box_x, box_y, box_w, box_h, color=(70, 70, 70), thickness=-1)
        frame.draw_rect(box_x, box_y, box_w, box_h, color=(255, 255, 255), thickness=2)

        frame.put_text(label, box_x + 20, box_y - 15, font_size=0.8, color=(255, 255, 255), thickness=2)

        score_text = str(self.game.scores[color].score)
        text_x = box_x + box_w // 2 - (20 if len(score_text) == 1 else 35)
        frame.put_text(score_text, text_x, box_y + box_h // 2 + 20, font_size=2.2, color=(255, 255, 255), thickness=3)

        if show_move_log:
            self._draw_move_log(frame, box_x, box_y + box_h, color)

    def _draw_move_log(self, frame, x, top_y, color):
        """מציירת את יומן המהלכים של הצבע הזה מתחת לפאנל הניקוד שלו - החדש ביותר למעלה, ללא גלילה."""
        y = top_y + 35
        for entry in self.move_log.entries_for(color):
            if y > self.board_pixels - 10:
                break
            frame.put_text(entry, x, y, font_size=MOVE_LOG_FONT_SIZE, color=MOVE_LOG_TEXT_COLOR, thickness=1)
            y += MOVE_LOG_LINE_HEIGHT
