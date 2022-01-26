from typing import Any, Dict, List

from pytris.board import Board
from pytris.tetromino import NAMES
from pytris.tetromino_queue import TetrominoQueue


class Tetris:
    def __init__(self) -> None:
        self.board = Board(10, 20)
        self.tetromino_queue = TetrominoQueue()
        self.tetromino_queue.update()
        self.current_tetromino = self.tetromino_queue.pop()
        self.y = -4
        self.x = 3

        self.held_tetromino = None
        self.can_hold = True

    def update(self) -> None:
        if not self.terminal:
            if len(self.tetromino_queue) <= len(NAMES):
                self.tetromino_queue.update()

            if not self.can_move_down:
                for i, j in self.current_tetromino.rotation:
                    self.board[self.y + j][self.x + i] = self.current_tetromino.name
                self.clear_rows()

                self.current_tetromino = self.tetromino_queue.pop()
                self.y = -4
                self.x = 3

                self.can_hold = True

    def drop_rows(self, cleared_rows: List[int]) -> None:
        for row in range(cleared_rows[-1] - 1, 0, -1):
            if self.board.is_empty(row):
                continue

            cur_row = row
            while self.board.is_empty(cur_row + 1):
                self.board.switch_rows(cur_row, cur_row + 1)
                cur_row += 1

    def clear_rows(self) -> None:
        if cleared_rows := self.board.full_rows:
            for row in cleared_rows:
                self.board[row].clear()

            self.drop_rows(cleared_rows)

    def move_down(self) -> None:
        if self.can_move_down:
            self.y += 1

    def move_right(self) -> None:
        if self.can_move_right:
            self.x += 1

    def move_left(self) -> None:
        if self.can_move_left:
            self.x -= 1

    def soft_drop(self) -> None:
        if self.can_move_right:
            self.x += 1

    def hard_drop(self) -> None:
        while self.can_move_down:
            self.y += 1

    def hold(self) -> None:
        if self.held_tetromino is None:
            self.held_tetromino, self.current_tetromino = self.current_tetromino, self.tetromino_queue.pop()
        elif self.can_hold:
            self.held_tetromino, self.current_tetromino = self.current_tetromino, self.held_tetromino
        self.can_hold = False

    @property
    def can_move_down(self) -> bool:
        return self.y + self.current_tetromino.bottom < self.board.height and \
               all(self.board[self.y + j + 1][self.x + i] is None for i, j in self.current_tetromino.rotation)

    @property
    def can_move_right(self) -> bool:
        return self.x + self.current_tetromino.right < self.board.width and \
               all(self.board[self.y + j][self.x + i + 1] is None for i, j in self.current_tetromino.rotation)

    @property
    def can_move_left(self) -> bool:
        return self.x + self.current_tetromino.left >= 0 and \
               all(self.board[self.y + j][self.x + i - 1] is None for i, j in self.current_tetromino.rotation)

    @property
    def terminal(self) -> bool:
        """ If the top row has any locked blocks in it, the game is over. """
        return not self.board.is_empty(0)

    def to_json(self) -> Dict[str, Any]:
        return {
            'x': self.x,
            'y': self.y,
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
