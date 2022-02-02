import os

import pygame as pg

from pytris import Tetris
from pyview.assets import Assets
from pyview.key import Key
from pyview.screen import Screen
from pyview.surface import Surface
from tetris.consts import Consts


class Game(Screen):
    def __init__(self) -> None:
        height = pg.display.Info().current_h
        super().__init__(int(height * 0.96), int(height * 0.8), fps=5)

        images = {name: Surface.load(os.path.join(Consts.images_directory, f'{name}.png'), 20, 20)
                  for name in ('O', 'I', 'T', 'L', 'J', 'S', 'Z', 'border', 'ghost')}
        self.images = Assets(images)

        self.tetris = Tetris()

    def draw_board_borders(self, x: float, y: float, board_width: int, board_height: int) -> None:
        border = self.images['border']
        for i in range(board_width):
            self.blit(border, x + i * border.width, y)

    def draw_board(self, board) -> None:
        self.draw_board_borders(200, 200, board['width'], board['height'])
        pass

    def draw_current_tetromino(self, current_tetromino) -> None:
        pass

    def update(self) -> None:
        self.fill((0, 0, 0))

        info = self.tetris.to_json()

        self.draw_board(info['board'])
        self.draw_current_tetromino(info['current_tetromino'])

        self.tetris.move_down()
        self.tetris.update()

    def key_down(self, key: Key) -> None:
        if key is Key.RIGHT_ARROW:
            self.tetris.move_right()
        elif key is Key.LEFT_ARROW:
            self.tetris.move_left()
        elif key is Key.SPACE:
            self.tetris.hard_drop()
        elif key is Key.DOWN_ARROW:
            self.tetris.soft_drop()
