from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

ROTATIONS = {
    'O': (
        ((0, 0), (1, 0), (0, 1), (1, 1)),
    ),
    'I': (
        ((0, 1), (1, 1), (2, 1), (3, 1)),
        ((1, 0), (1, 1), (1, 2), (1, 3)),
        ((0, 2), (1, 2), (2, 2), (3, 2)),
        ((2, 0), (2, 1), (2, 2), (2, 3)),
    ),
    'T': (
        ((1, 0), (0, 1), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (2, 1), (1, 2)),
        ((0, 1), (1, 1), (2, 1), (1, 2)),
        ((1, 0), (1, 1), (1, 2), (0, 1)),
    ),
    'S': (
        ((1, 0), (2, 0), (0, 1), (1, 1)),
        ((1, 0), (1, 1), (2, 1), (2, 2)),
        ((1, 1), (2, 1), (0, 2), (1, 2)),
        ((0, 0), (0, 1), (1, 1), (1, 2)),
    ),
    'Z': (
        ((0, 0), (1, 0), (1, 1), (2, 1)),
        ((2, 0), (1, 1), (2, 1), (1, 2)),
        ((0, 1), (1, 1), (1, 2), (2, 2)),
        ((1, 0), (1, 1), (0, 1), (0, 2)),
    ),
    'L': (
        ((0, 1), (1, 1), (2, 1), (0, 0)),
        ((1, 0), (1, 1), (1, 2), (2, 0)),
        ((0, 1), (1, 1), (2, 1), (2, 2)),
        ((1, 0), (1, 1), (1, 2), (0, 2)),
    ),
    'J': (
        ((0, 1), (1, 1), (2, 1), (2, 0)),
        ((1, 0), (1, 1), (1, 2), (2, 2)),
        ((0, 1), (1, 1), (2, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2), (0, 0)),
    ),
}
NAMES = list(ROTATIONS.keys())
Block = Tuple[int, int]
Rotation = Tuple[Block, Block, Block, Block]
Rotations = Tuple[Rotation, ...]


@dataclass
class Tetromino:
    name: str
    rotation_index: int = field(init=False, default=0)

    @property
    def rotations(self) -> Rotations:
        return ROTATIONS[self.name]

    @property
    def rotation(self) -> Rotation:
        """ Returns the current rotation of the Tetromino. """
        return self.rotations[self.rotation_index]

    @property
    def right(self) -> int:
        """ Returns the right index in the current rotation. """
        return max(i for i, j in self.rotation)

    @property
    def left(self) -> int:
        """ Returns the left index in the current rotation. """
        return min(i for i, j in self.rotation)

    @property
    def top(self) -> int:
        """ Returns the top index in the current rotation. """
        return min(j for i, j in self.rotation)

    @property
    def bottom(self) -> int:
        """ Returns the bottom index in the current rotation. """
        return max(j for i, j in self.rotation)

    @property
    def width(self) -> int:
        """ Returns the width of the Tetromino. """
        return abs(self.left - self.right) + 1

    @property
    def height(self) -> int:
        """ Returns the height of the Tetromino. """
        return abs(self.top - self.bottom) + 1

    def to_json(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'rotation': self.rotation,
            'width': self.width,
            'height': self.height,
        }
