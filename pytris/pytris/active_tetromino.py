from dataclasses import dataclass, replace
from functools import cached_property
from typing import Any, Dict, Tuple

from pytris.tetromino import ROTATIONS, Tetromino

general_rotation_offsets = {
    (0, 1): ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
    (1, 0): ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
    (1, 2): ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
    (2, 1): ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
    (2, 3): ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
    (3, 2): ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
    (3, 0): ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
    (0, 3): ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
}
ROTATION_OFFSETS = {
    'J': general_rotation_offsets,
    'L': general_rotation_offsets,
    'T': general_rotation_offsets,
    'S': general_rotation_offsets,
    'Z': general_rotation_offsets,
    'O': {
        (0, 0): ((0, 0),),
    },
    'I': {
        (0, 1): ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),
        (1, 0): ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
        (1, 2): ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)),
        (2, 1): ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
        (2, 3): ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
        (3, 2): ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),
        (3, 0): ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
        (0, 3): ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)),
    }
}


@dataclass
class ActiveTetromino(Tetromino):
    x: int
    y: int

    @cached_property
    def num_of_rotations(self) -> int:
        return len(ROTATIONS[self.name])

    @property
    def right_rotation_index(self) -> int:
        return (self.rotation_index + 1) % self.num_of_rotations

    @property
    def right_rotation(self) -> Tuple[Tuple[int, int], ...]:
        return ROTATIONS[self.name][self.right_rotation_index]

    @property
    def left_rotation_index(self) -> int:
        return (self.rotation_index + 1) % self.num_of_rotations

    @property
    def left_rotation(self) -> Tuple[Tuple[int, int], ...]:
        return ROTATIONS[self.name][self.left_rotation_index]

    @property
    def right_rotation_offsets(self) -> Tuple[Tuple[int, int], ...]:
        return ROTATION_OFFSETS[self.name][self.rotation_index, self.right_rotation_index]

    @property
    def left_rotation_offsets(self) -> Tuple[Tuple[int, int], ...]:
        return ROTATION_OFFSETS[self.name][self.rotation_index, self.left_rotation_index]

    @property
    def right(self) -> int:
        """ Returns the right index in the current rotation. """
        return self.x + super().right

    @property
    def left(self) -> int:
        """ Returns the left index in the current rotation. """
        return self.x + super().left

    @property
    def top(self) -> int:
        """ Returns the top index in the current rotation. """
        return self.y + super().top

    @property
    def bottom(self) -> int:
        """ Returns the bottom index in the current rotation. """
        return self.y + super().bottom

    def move_down(self) -> None:
        self.y += 1

    def move_right(self) -> None:
        self.x += 1

    def move_left(self) -> None:
        self.x -= 1

    def rotate_right(self) -> None:
        self.rotation_index = self.right_rotation_index

    def rotate_left(self) -> None:
        self.rotation_index = self.left_rotation_index

    def copy(self) -> 'ActiveTetromino':
        copy = replace(self)
        copy.rotation_index = self.rotation_index
        return copy

    @classmethod
    def from_tetromino(cls, tetromino: Tetromino, x: int, y: int) -> 'ActiveTetromino':
        return cls(tetromino.name, x, y)

    def to_json(self) -> Dict[str, Any]:
        return {
            'x': self.x,
            'y': self.y,
            **super().to_json()
        }
