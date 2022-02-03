from typing import Any, Dict, List, Tuple

from pytris.active_tetromino import ActiveTetromino
from pytris.board import Board
from pytris.tetromino import NAMES, Tetromino
from pytris.tetromino_queue import TetrominoQueue


class Tetris:
    def __init__(self) -> None:
        self.board = Board(10, 20)
        self.tetromino_queue = TetrominoQueue()
        self.tetromino_queue.update()
        self.current_tetromino = ActiveTetromino.from_tetromino(self.tetromino_queue.pop(), 3, -4)

        self.held_tetromino = None
        self.can_hold = True

    def update(self) -> None:
        if not self.terminal:
            if len(self.tetromino_queue) <= len(NAMES):
                self.tetromino_queue.update()

            if not self.can_move_down:
                for i, j in self.current_tetromino.rotation:
                    self.board[self.current_tetromino.y + j][self.current_tetromino.x + i] = self.current_tetromino.name
                self.clear_rows()

                self.current_tetromino = ActiveTetromino.from_tetromino(self.tetromino_queue.pop(), 3, -4)

                self.can_hold = True

    def drop_rows(self, cleared_rows: List[int]) -> None:
        for row in range(cleared_rows[-1] - 1, 0, -1):
            if self.board.is_empty(row):
                continue

            cur_row = row
            while cur_row + 1 < self.board.height and self.board.is_empty(cur_row + 1):
                self.board.switch_rows(cur_row, cur_row + 1)
                cur_row += 1

    def clear_rows(self) -> None:
        if cleared_rows := self.board.full_rows:
            for row in cleared_rows:
                self.board[row].clear()

            self.drop_rows(cleared_rows)

    def move_down(self) -> None:
        if self.can_move_down:
            self.current_tetromino.move_down()

    def move_right(self) -> None:
        if self.can_move_right:
            self.current_tetromino.move_right()

    def move_left(self) -> None:
        if self.can_move_left:
            self.current_tetromino.move_left()

    def rotate_right(self) -> None:
        for x_offset, y_offset in self.current_tetromino.right_rotation_offsets:
            if self.can_rotate(self.current_tetromino.right_rotation, x_offset, y_offset):
                self.current_tetromino.rotate_right()

    def rotate_left(self) -> None:
        for x_offset, y_offset in self.current_tetromino.left_rotation_offsets:
            if self.can_rotate(self.current_tetromino.left_rotation, x_offset, y_offset):
                self.current_tetromino.rotate_left()

    def soft_drop(self) -> None:
        if self.can_move_right:
            self.current_tetromino.y += 1

    def hard_drop(self) -> None:
        while self.can_move_down:
            self.current_tetromino.y += 1

    def hold(self) -> None:
        if self.can_hold:
            if self.held_tetromino is None:
                new_tetromino = self.tetromino_queue.pop()
            else:
                new_tetromino = self.held_tetromino

            self.held_tetromino = Tetromino(self.current_tetromino.name)
            self.current_tetromino = ActiveTetromino.from_tetromino(new_tetromino, 3, -4)
            self.can_hold = False

    @property
    def can_move_down(self) -> bool:
        if self.current_tetromino.bottom < 0:
            return True
        return self.current_tetromino.bottom + 1 < self.board.height and \
               all(self.board[self.current_tetromino.y + j + 1][self.current_tetromino.x + i] is None
                   for i, j in self.current_tetromino.rotation if self.current_tetromino.y + j >= 0)

    @property
    def can_move_right(self) -> bool:
        return self.current_tetromino.right + 1 < self.board.width and \
               all(self.board[self.current_tetromino.y + j][self.current_tetromino.x + i + 1] is None
                   for i, j in self.current_tetromino.rotation)

    @property
    def can_move_left(self) -> bool:
        return self.current_tetromino.left > 0 and \
               all(self.board[self.current_tetromino.y + j][self.current_tetromino.x + i - 1] is None
                   for i, j in self.current_tetromino.rotation)

    def can_rotate(self, rotation: Tuple[Tuple[int, int], ...], x_offset: int, y_offset: int) -> bool:
        return all(0 < self.current_tetromino.y + j + y_offset < self.board.height and
                   0 < self.current_tetromino.x + i + x_offset < self.board.width and
                   self.board[self.current_tetromino.y + j + y_offset][self.current_tetromino.x + i + x_offset] is None
                   for i, j in rotation)

    @property
    def terminal(self) -> bool:
        """ If the top row has any locked blocks in it, the game is over. """
        return not self.board.is_empty(0)

    def to_json(self) -> Dict[str, Any]:
        return {
            'current_tetromino': self.current_tetromino.to_json(),
            'held_tetromino': self.held_tetromino.to_json() if self.held_tetromino else None,
            'tetromino_queue': self.tetromino_queue.to_json(),
            'board': self.board.to_json(),
            'stats': {
                'cleared_rows': 0,
                'level': 0,
                'score': 0,
                'high_score': 0,
            },
        }
