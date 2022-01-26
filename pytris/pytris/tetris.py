from pytris.board import Board
from pytris.tetromino import NAMES
from pytris.tetromino_queue import TetrominoQueue


class Tetris:
    def __init__(self) -> None:
        self.board = Board(10, 20)
        self.tetromino_queue = TetrominoQueue()
        self.tetromino_queue.update()
        self.cur_tetromino = self.tetromino_queue.pop()
        self.y = -4
        self.x = 3
        self.held_tetromino = None

    def update(self) -> None:
        if not self.terminal:
            if len(self.tetromino_queue) <= len(NAMES):
                self.tetromino_queue.update()

    def move_down(self) -> None:
        if self.can_move_down:
            self.y += 1

    def move_right(self) -> None:
        if self.can_move_right:
            self.x += 1

    def move_left(self) -> None:
        if self.can_move_left:
            self.x -= 1

    def hard_drop(self) -> None:
        while self.can_move_down:
            self.y += 1

    @property
    def can_move_down(self) -> bool:
        return self.y + self.cur_tetromino.bottom < self.board.height and \
               all(self.board[self.y + j + 1][self.x + i] is None for i, j in self.cur_tetromino.rotation)

    @property
    def can_move_right(self) -> bool:
        return self.x + self.cur_tetromino.right < self.board.width and \
               all(self.board[self.y + j][self.x + i - 1] is None for i, j in self.cur_tetromino.rotation)

    @property
    def can_move_left(self) -> bool:
        return self.x + self.cur_tetromino.left >= 0 and \
               all(self.board[self.y + j][self.x + i - 1] is None for i, j in self.cur_tetromino.rotation)

    @property
    def terminal(self) -> bool:
        """ If the top row has any locked blocks in it, the game is over. """
        return not self.board.is_empty(index=0)

    @property
    def locked(self) -> bool:
        return False
