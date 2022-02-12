from typing import Dict, Iterable, Tuple

from pytris.controller import TetrisController
from pyview import DISPLAY_HEIGHT
from pyview.key import Key
from pyview.screen import Screen
from pyview.surface import Surface
from tetris.assets import Colors, Images
from tetris.consts import Consts


class Border(Surface):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width * Consts.block_size, height * Consts.block_size)
        self.fill(Colors.transparent)
        for i in range(width + 2):
            self.blit(Images.border, i * Consts.block_size, 0)
            self.blit(Images.border, i * Consts.block_size, (height - 1) * Consts.block_size)
        for j in range(1, height - 1):
            self.blit(Images.border, 0, j * Consts.block_size)
            self.blit(Images.border, (width - 1) * Consts.block_size, j * Consts.block_size)

    def reset(self) -> None:
        self.fill(Colors.transparent, Consts.block_size, Consts.block_size, self.width - Consts.block_size * 2,
                  self.height - Consts.block_size * 2)

    def draw_tetromino(self, name: str, x: int, y: int, rotation: Iterable[Tuple[int, int]]) -> None:
        for i, j in rotation:
            if y + j + 1 > 0:
                self.blit(Images[name], (x + i + 1) * Consts.block_size, (y + j + 1) * Consts.block_size)


class Game(Screen):
    def __init__(self) -> None:
        super().__init__(DISPLAY_HEIGHT, DISPLAY_HEIGHT * 0.75, fps=100)

        self.board = Border(12, 22)

        self.tetris = TetrisController(10, 20)

    def draw_board(self, info: Dict) -> None:
        self.board.reset()
        for j, row in enumerate(info['board']['cells']):
            for i, cell in enumerate(row):
                if cell is None:
                    continue

                image = Images[cell]
                self.board.blit(image, (i + 1) * Consts.block_size, (j + 1) * Consts.block_size)

        ghost_tetromino = info['ghost_tetromino']
        self.board.draw_tetromino('ghost', ghost_tetromino['x'], ghost_tetromino['y'], ghost_tetromino['rotation'])
        current_tetromino = info['current_tetromino']
        self.board.draw_tetromino(current_tetromino['name'], current_tetromino['x'], current_tetromino['y'],
                                  current_tetromino['rotation'])
        self.blit(self.board, self.width * .5, self.height * .5, centered=True)

    def update(self) -> None:
        self.fill(Colors.black)
        info = self.tetris.to_json()
        self.draw_board(info)

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
