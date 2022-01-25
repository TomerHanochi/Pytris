from pytris.board import Board
from pytris.cooldown import cooldown
from pytris.tetromino import Tetromino
from pytris.tetromino_queue import TetrominoQueue


class Tetris:
    def __init__(self) -> None:
        self.board = Board(10, 20)
        self.tetromino_queue = TetrominoQueue()
        self.tetromino_queue.update()
        self.cur_tetromino = Tetromino(self.tetromino_queue.pop())
        self.held_tetromino = None

        self.should_move_left = False
        self.should_move_right = False
        self.should_soft_drop = False

    def update(self) -> None:
        if self.terminal:
            pass
        else:
            if len(self.tetromino_queue) < len(Tetromino.rotations.keys()):
                self.tetromino_queue.update()

            for i, j in self.cur_tetromino.rotation:
                self.board[self.cur_tetromino.y + j][self.cur_tetromino.x + i] = self.cur_tetromino.name

            cleared = self.board.clear_rows()
            if cleared:
                pass

            if self.should_move_left:
                self.move_left()

            if self.should_move_right:
                self.move_right()

            if self.should_soft_drop:
                self.soft_drop()

            if self.locked:
                self.cur_tetromino = Tetromino(self.tetromino_queue.pop())

            self.move_down()

    def move_down(self) -> None:
        pass

    @cooldown(duration=0.05)
    def move_right(self) -> None:
        pass

    @cooldown(duration=0.05)
    def move_left(self) -> None:
        pass

    @cooldown(duration=0.05)
    def soft_drop(self) -> None:
        pass

    @property
    def terminal(self) -> bool:
        """ If the top row has any locked blocks in it, the game is over. """
        return not self.board[0].is_empty

    @property
    def locked(self) -> bool:
        return False
