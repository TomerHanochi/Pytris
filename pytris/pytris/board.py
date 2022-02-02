from typing import Any, Dict, List, Optional

from pytris.generic_data_structures import Array


class Board(Array[Array[Optional[str]]]):
    def __init__(self, width: float, height: float) -> None:
        super().__init__(Array(None for _ in range(width)) for _ in range(height))
        self.__width = width
        self.__height = height

    def is_empty(self, row: int) -> bool:
        return all(cell is None for cell in self[row])

    def is_full(self, row: int) -> bool:
        return all(cell is not None for cell in self[row])

    def switch_rows(self, row1: int, row2: int) -> None:
        self[row1], self[row2] = self[row2], self[row1]

    @property
    def full_rows(self) -> List[int]:
        return [row for row in range(self.height) if self.is_full(row)]

    def to_json(self) -> Dict[str, Any]:
        return {
            'width': self.width,
            'height': self.height,
            'cells': [[cell for cell in row] for row in self],
        }

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height
