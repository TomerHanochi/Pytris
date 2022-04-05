import os
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
        super().__init__(x, y, width=width * Consts.block_size, height=height * Consts.block_size + self.offset,
                         centered=centered)
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
        self.fill(Colors.transparent, Consts.block_size, Consts.block_size + self.offset,
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
    font_size = Consts.block_size * 0.75
    spacing = Consts.block_size * 1.5

    def __init__(self, x: float, y: float, centered: bool = False) -> None:
        super().__init__(x, y, centered=centered, surface=Fonts.pixel.render(text='CLEARED LINES\nLEVEL\nSCORE\nHIGH SCORE\n',
                                                                             color=Colors.white,
                                                                             size=self.font_size,
                                                                             spacing=self.spacing,
                                                                             align='ltr'))

    def update(self, info: Dict) -> None:
        for i, stat_value in enumerate(info['stats'].values()):
            stat = Fonts.pixel.render(f'{stat_value}', Colors.white, self.font_size)
            self.fill(Colors.transparent, 0, (i + 1) * self.font_size + i * self.spacing, self.width, self.spacing)
            self.blit(stat, 0, (i + 1) * self.font_size + (i + .5) * self.spacing - stat.height * .5)


class Game(Screen):
    def __init__(self) -> None:
        super().__init__(Consts.game_screen_width, Consts.game_screen_height, fps=100)
        self.block_size = self.height * 0.8 // (Consts.board_height + 2)

    def blit_board(self, info: Dict) -> None:
        self.board.reset()

        self.board.draw_cells(info['board']['cells'])

        ghost_tetromino = info['ghost_tetromino']
        self.board.draw_tetromino('ghost', ghost_tetromino['x'] * Consts.block_size, ghost_tetromino['y'] * Consts.block_size,
                                  ghost_tetromino['visible_rotation'])
        current_tetromino = info['current_tetromino']
        self.board.draw_tetromino(current_tetromino['name'], current_tetromino['x'] * Consts.block_size,
                                  current_tetromino['y'] * Consts.block_size, current_tetromino['visible_rotation'])
        self.blit_widget(self.board)

    def blit_next(self, info: Dict) -> None:
        self.next.reset()
        for i, tetromino in enumerate(info['tetromino_queue'][:Consts.next_size]):
            self.next.draw_tetromino(tetromino['name'], (self.next.width - (tetromino['width'] + 2) * Consts.block_size) * .5,
                                     (i * 3 + 1) * Consts.block_size, tetromino['rotation'])
        self.blit_widget(self.next)

    def blit_held(self, info: Dict) -> None:
        self.held.reset()
        tetromino = info['held_tetromino']
        if tetromino is not None:
            self.held.draw_tetromino(tetromino['name'], (self.held.width - (tetromino['width'] + 2) * Consts.block_size) * .5,
                                     Consts.block_size, tetromino['rotation'])
        self.blit_widget(self.held)

    def blit_stats(self, info: Dict) -> None:
        self.stats.update(info)
        self.blit_widget(self.stats)

    def update(self) -> None:
        self.fill(Colors.black)

        info = self.tetris.to_json()
        self.blit_board(info)
        self.blit_next(info)
        self.blit_held(info)
        self.blit_stats(info)
        self.blit_widget(self.reset_button)
        self.blit_widget(self.ai_switch)
        self.blit_widget(self.back)

        self.tetris.update()

    def mouse_down(self, x: float, y: float) -> None:
        if self.reset_button.overlap(x, y):
            self.tetris.update_high_score()
            self.tetris.reset()
        elif self.ai_switch.overlap(x, y):
            self.tetris.switch_use_ai()
        elif self.back.overlap(x, y):
            self.redirect('MainMenu')

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
                      title=Fonts.pixel.render('TETRIS', Colors.white, 2.125 * Consts.block_size),
                      centered=True)

    @cached_property
    def held(self) -> Border:
        widget = Border(x=self.board.right + Consts.block_size,
                        y=self.board.top + self.board.offset,
                        width=7,
                        height=6,
                        title=Fonts.pixel.render('HELD', Colors.white, 1.25 * Consts.block_size))
        widget.y -= widget.offset
        return widget

    @cached_property
    def next(self) -> Border:
        widget = Border(x=self.board.left - 8 * Consts.block_size,
                        y=self.board.top + self.board.offset,
                        width=7,
                        height=(Consts.next_size + 1) * 3,
                        title=Fonts.pixel.render('NEXT', Colors.white, 1.25 * Consts.block_size))
        widget.y -= widget.offset
        return widget

    @cached_property
    def stats(self) -> Stats:
        return Stats(x=self.board.right + Consts.block_size,
                     y=self.held.bottom + Consts.block_size)

    @cached_property
    def reset_button(self) -> Widget:
        return Widget(x=self.board.right + Consts.block_size,
                      y=self.stats.bottom + Consts.block_size,
                      surface=Fonts.pixel.render(text='RESET', color=Colors.black, size=Consts.block_size * 1.5,
                                                 background=Colors.white))

    @cached_property
    def ai_switch(self) -> Widget:
        return Widget(x=self.reset_button.x,
                      y=self.reset_button.bottom + Consts.block_size,
                      surface=Fonts.pixel.render(text='USE AI', color=Colors.black, size=Consts.block_size * 1.5,
                                                 background=Colors.white))

    @cached_property
    def back(self) -> Widget:
        return Widget(x=self.width * 0.01, y=self.board.y, surface=Images.back)

    @cached_property
    def tetris(self) -> TetrisController:
        return TetrisController(width=Consts.board_width,
                                height=Consts.board_height,
                                high_score_filepath=os.path.join(Consts.base_path, 'high_score.txt'))
