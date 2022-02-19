from functools import cached_property
from typing import Dict, Iterable, Tuple

from pytris.controller import TetrisController
from pyview.key import Key
from pyview.screen import Screen
from pyview.surface import Surface
from pyview.widget import Widget
from tetris.assets import Colors, Fonts, Images
from tetris.consts import Consts


class Border(Widget):
    def __init__(self, x: float, y: float, width: int, height: int, title: Surface = None, centered: bool = False) -> None:
        self.offset = 0 if title is None else title.height + Consts.block_size
        super().__init__(x, y, width * Consts.block_size, height * Consts.block_size + self.offset, centered=centered)
        self.fill(Colors.transparent)

        if title is not None:
            self.blit(title, self.width * .5, title.height * .5, centered=True)

        for i in range(width + 2):
            self.blit(Images.border, i * Consts.block_size, self.offset)
            self.blit(Images.border, i * Consts.block_size, (height - 1) * Consts.block_size + self.offset)
        for j in range(1, height - 1):
            self.blit(Images.border, 0, j * Consts.block_size + self.offset)
            self.blit(Images.border, (width - 1) * Consts.block_size, j * Consts.block_size + self.offset)

    def reset(self) -> None:
        self.fill(Colors.transparent, Consts.block_size, self.offset + Consts.block_size,
                  self.width - Consts.block_size * 2, self.height - Consts.block_size * 2 - self.offset)

    def draw_cells(self, cells: Iterable[Iterable[str]]) -> None:
        for j, row in enumerate(cells):
            for i, cell in enumerate(row):
                if cell is None:
                    continue

                image = Images[cell]
                self.blit(image, (i + 1) * Consts.block_size, (j + 1) * Consts.block_size + self.offset)

    def draw_tetromino(self, name: str, x: float, y: float, rotation: Iterable[Tuple[int, int]]) -> None:
        for i, j in rotation:
            self.blit(Images[name], x + (i + 1) * Consts.block_size, y + (j + 1) * Consts.block_size + self.offset)


class Stats(Widget):
    font_size = Consts.block_size * 1.25
    stats = {
        'cleared_lines': Fonts.pixel.render('CLEARED LINES', Colors.white, font_size),
        'level': Fonts.pixel.render('LEVEL', Colors.white, font_size),
        'score': Fonts.pixel.render('SCORE', Colors.white, font_size),
    }

    def __init__(self, x: float, y: float, centered: bool = False) -> None:
        super().__init__(x, y, max(s.width for s in self.stats.values()), self.font_size * 6, centered=centered)
        self.fill(Colors.transparent)
        for i, stat in enumerate(self.stats.values()):
            self.blit(stat, 0, 2 * i * self.font_size)

    def update(self, info: Dict) -> None:
        for i, stat_value in enumerate(info['stats'].values()):
            stat = Fonts.pixel.render(f'{stat_value}', Colors.white, self.font_size)
            self.fill(Colors.transparent, 0, (2 * i + 1) * self.font_size, self.width, self.font_size)
            self.blit(stat, 0, (2 * i + 1) * self.font_size)


class Game(Screen):
    def __init__(self) -> None:
        super().__init__(Consts.game_screen_width, Consts.game_screen_height, fps=100)
        self.block_size = self.height * 0.8 // (Consts.board_height + 2)

    def draw_board(self, info: Dict) -> None:
        self.board.reset()

        self.board.draw_cells(info['board']['cells'])

        ghost_tetromino = info['ghost_tetromino']
        self.board.draw_tetromino('ghost', ghost_tetromino['x'] * Consts.block_size, ghost_tetromino['y'] * Consts.block_size,
                                  ghost_tetromino['rotation'])
        current_tetromino = info['current_tetromino']
        self.board.draw_tetromino(current_tetromino['name'], current_tetromino['x'] * Consts.block_size,
                                  current_tetromino['y'] * Consts.block_size, current_tetromino['visible_rotation'])
        self.blit(self.board, self.board.x, self.board.y)

    def draw_next(self, info: Dict) -> None:
        self.next.reset()
        for i, tetromino in enumerate(info['tetromino_queue'][:Consts.next_size]):
            self.next.draw_tetromino(tetromino['name'], (self.next.width - (tetromino['width'] + 2) * Consts.block_size) * .5,
                                     (i * 3 + 1) * Consts.block_size, tetromino['rotation'])
        self.blit(self.next, self.next.x, self.next.y)

    def draw_held(self, info: Dict) -> None:
        self.held.reset()
        tetromino = info['held_tetromino']
        if tetromino is not None:
            self.held.draw_tetromino(tetromino['name'], (self.held.width - (tetromino['width'] + 2) * Consts.block_size) * .5,
                                     Consts.block_size, tetromino['rotation'])
        self.blit(self.held, self.held.x, self.held.y)

    def draw_stats(self, info: Dict) -> None:
        self.stats.update(info)
        self.blit(self.stats, self.stats.x, self.stats.y)

    def update(self) -> None:
        self.fill(Colors.black)

        info = self.tetris.to_json()
        self.draw_board(info)
        self.draw_next(info)
        self.draw_held(info)
        self.draw_stats(info)
        self.blit(self.reset_button, self.reset_button.x, self.reset_button.y)

        self.tetris.update()

    def mouse_down(self, x: float, y: float) -> None:
        if self.reset_button.overlap(x, y):
            self.tetris.reset()

    def key_down(self, key: Key) -> None:
        if key is Key.RIGHT_ARROW:
            self.tetris.start_move_right()
        elif key is Key.LEFT_ARROW:
            self.tetris.start_move_left()
        elif key is Key.SPACE:
            self.tetris.hard_drop()
        elif key is Key.DOWN_ARROW:
            self.tetris.start_soft_drop()
        elif key in {Key.UP_ARROW, Key.X}:
            self.tetris.start_rotate_right()
        elif key in {Key.CTRL, Key.Z}:
            self.tetris.start_rotate_left()
        elif key in {Key.SHIFT, Key.C}:
            self.tetris.hold()
        elif key in {Key.ESCAPE, Key.F1}:
            self.tetris.pause_or_resume()

    def key_up(self, key: Key) -> None:
        if key is Key.RIGHT_ARROW:
            self.tetris.stop_move_right()
        elif key is Key.LEFT_ARROW:
            self.tetris.stop_move_left()
        elif key is Key.DOWN_ARROW:
            self.tetris.stop_soft_drop()
        elif key in {Key.UP_ARROW, Key.X}:
            self.tetris.stop_rotate_right()
        elif key in {Key.CTRL, Key.Z}:
            self.tetris.stop_rotate_left()

    @cached_property
    def board(self) -> Border:
        return Border(x=self.width * .5,
                      y=self.height * .5,
                      width=Consts.board_width + 2,
                      height=Consts.board_height + 2,
                      title=Fonts.pixel.render('TETRIS', Colors.white, 4.25 * Consts.block_size),
                      centered=True)

    @cached_property
    def held(self) -> Border:
        widget = Border(x=self.board.right + Consts.block_size,
                        y=self.board.top + self.board.offset,
                        width=7,
                        height=6,
                        title=Fonts.pixel.render('HELD', Colors.white, 2.5 * Consts.block_size))
        widget.y -= widget.offset
        return widget

    @cached_property
    def next(self) -> Border:
        widget = Border(x=self.board.left - 8 * Consts.block_size,
                        y=self.board.top + self.board.offset,
                        width=7,
                        height=(Consts.next_size + 1) * 3,
                        title=Fonts.pixel.render('NEXT', Colors.white, 2.5 * Consts.block_size))
        widget.y -= widget.offset
        return widget

    @cached_property
    def stats(self) -> Stats:
        return Stats(x=self.board.right + Consts.block_size,
                     y=self.held.bottom + Consts.block_size)

    @cached_property
    def reset_button(self) -> Widget:
        return Widget(x=self.board.right + Consts.block_size,
                      y=self.stats.bottom,
                      surface=Fonts.pixel.render('RESET', Colors.black, Consts.block_size * 3, background=Colors.white))

    @cached_property
    def tetris(self) -> TetrisController:
        return TetrisController(Consts.board_width, Consts.board_height)
