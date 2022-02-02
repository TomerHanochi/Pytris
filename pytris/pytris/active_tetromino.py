from dataclasses import dataclass
from typing import Any, Dict

from pytris.tetromino import Tetromino


@dataclass
class ActiveTetromino(Tetromino):
    x: int
    y: int

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

    @classmethod
    def from_tetromino(cls, tetromino: Tetromino, x: int, y: int) -> 'ActiveTetromino':
        return cls(tetromino.name, x, y)

    def to_json(self) -> Dict[str, Any]:
        return {
            'x': self.x,
            'y': self.y,
            **super().to_json()
        }
