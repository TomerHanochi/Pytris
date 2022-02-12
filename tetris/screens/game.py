import os
from typing import Dict

from pytris.controller import TetrisController
from pyview.assets import Assets
from pyview.key import Key
from pyview.screen import Screen
from pyview.surface import Surface
from tetris.consts import Consts


class Board(Surface):
    def __init__(self, width: int, height: int, block_size: int) -> None:
        super().__init__((width + 2) * block_size, (height + 2) * block_size)
        self.images = Assets[str, Surface]({name: Surface.load(os.path.join(Consts.images_directory, f'{name}.png'),
                                                               block_size, block_size)
                                            for name in ('O', 'I', 'T', 'L', 'J', 'S', 'Z', 'border', 'ghost')})
        self.block_size = block_size
        self.background_color = (0, 0, 0, 0)
        # draws the board border
        self.fill(self.background_color)
        for i in range(width + 2):
            self.blit(self.images.border, i * block_size, 0)
            self.blit(self.images.border, i * block_size, (height + 1) * block_size)
        for j in range(1, height + 1):
            self.blit(self.images.border, 0, j * block_size)
            self.blit(self.images.border, (width + 1) * block_size, j * block_size)

    def update(self, info: Dict) -> None:
        self.fill(self.background_color, self.block_size, self.block_size,
                  self.width - 2 * self.block_size, self.height - 2 * self.block_size)
        board = info['board']
        for j, row in enumerate(board['cells']):
            for i, cell in enumerate(row):
                if cell is None:
                    continue

                image = self.images[cell]
                self.blit(image, (i + 1) * self.block_size, (j + 1) * self.block_size)

        current_tetromino = info['current_tetromino']
        image = self.images[current_tetromino['name']]
        x = current_tetromino['x']
        y = current_tetromino['y']
        for i, j in current_tetromino['rotation']:
            if y + j + 1 > 0:
                self.blit(image, (x + i + 1) * self.block_size, (y + j + 1) * self.block_size)


class Game(Screen):
    def __init__(self) -> None:
        height = Consts.display_height * 0.9
        width = height * 4 / 3  # 4:3 ratio
        super().__init__(width, height, fps=60)

        self.board = Board(width=10, height=20, block_size=40)

        self.tetris = TetrisController(10, 20)

    def update(self) -> None:
        self.fill((0, 0, 0))

        info = self.tetris.to_json()
        self.board.update(info)
        self.blit(self.board, self.width * .5, self.height * .5, centered=True)

        self.tetris.update()

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
