from dataclasses import dataclass
from math import inf
from typing import Generator, Tuple

from pytris import Tetris
from pytris.active_tetromino import ActiveTetromino
from pytris.ai.network import Network
from pytris.board import Board


@dataclass(frozen=True)
class Move:
    rotation: int = 0
    right: int = 0
    left: int = 0


def get_right(tetromino, rotation) -> int:
    """ Returns the amount of blocks the tetromino can move right. """
    return 10 - (tetromino.x + max(i for i, j in tetromino.rotations[rotation]))


def get_left(tetromino, rotation) -> int:
    """ Returns the amount of blocks the tetromino can move left. """
    return tetromino.x + min(i for i, j in tetromino.rotations[rotation]) + 1


def get_moves(tetromino: ActiveTetromino) -> Generator[Move, None, None]:
    """ Generates all possibl moves for the tetromino. """
    for rotation in range(tetromino.num_of_rotations):
        yield Move(rotation)
        for right in range(1, get_right(tetromino, rotation)):
            yield Move(rotation, right=right)
        for left in range(1, get_left(tetromino, rotation)):
            yield Move(rotation, left=left)


def do_move(tetris: Tetris, move: Move) -> None:
    for _ in range(move.rotation):
        tetris.rotate_right()

    for _ in range(move.right):
        tetris.move_right()

    for _ in range(move.left):
        tetris.move_left()

    tetris.hard_drop()

    tetromino = tetris.current_tetromino
    for i, j in tetromino.rotation:
        if tetromino.y + j >= 0:
            tetris.board[tetromino.y + j][tetromino.x + i] = tetromino.name


def score_board(board: Board, network: Network) -> float:
    aggregate_height = 0
    bumpiness = 0
    holes = 0
    prev_col_height = None
    for col in zip(*board):
        col_height = 0
        for i, cell in enumerate(col):
            if col_height == 0 and cell is not None:
                col_height = board.height - i

            if i > 0 and col[i - 1] is not None and cell is None:
                holes += 1

        aggregate_height += col_height
        if prev_col_height is not None:
            bumpiness += abs(col_height - prev_col_height)

        prev_col_height = col_height

    cleared_lines = sum(1 for row in range(board.height) if board.is_full(row))
    return network.weights.dot((aggregate_height, cleared_lines, holes, bumpiness))


def undo_move(tetris: Tetris, copy: ActiveTetromino) -> None:
    tetromino = tetris.current_tetromino
    for i, j in tetromino.rotation:
        if tetromino.y + j >= 0:
            tetris.board[tetromino.y + j][tetromino.x + i] = None

    tetromino.x = copy.x
    tetromino.y = copy.y
    tetromino.rotation_index = copy.rotation_index


def _best_move(tetris: Tetris, network: Network):
    """ Finds the best move according to the current tetromino. """
    best_move = None
    best_score = -inf
    copy = tetris.current_tetromino.copy()
    for move in get_moves(tetris.current_tetromino):
        do_move(tetris, move)
        score = score_board(tetris.board, network)
        undo_move(tetris, copy)

        if score > best_score:
            best_move = move
            best_score = score
    return best_move, best_score


def generate_best_move(tetris: Tetris, network: Network) -> Tuple[Move, bool]:
    """ Returns the best move according to the current and held/next tetromino. """
    tetris_score = tetris.score
    best_move, best_score = _best_move(tetris, network)
    tetris.hold()
    alt_best_move, alt_best_score = _best_move(tetris, network)
    tetris.unhold()
    use_alt_move = best_score < alt_best_score
    tetris.score = tetris_score
    return alt_best_move if use_alt_move else best_move, use_alt_move
