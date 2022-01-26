from typing import Iterator, Optional, List


class Board:
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__cells = [[None for _ in range(width)] for _ in range(height)]

    def __getitem__(self, index: int) -> List[Optional[str]]:
        return self.__cells[index]

    def __setitem__(self, index: int, value: List[Optional[str]]) -> None:
        self.__cells[index] = value

    def __iter__(self) -> Iterator[List[Optional[str]]]:
        return iter(self.__cells)

    def __len__(self) -> int:
        return len(self.__cells)

    def __repr__(self) -> str:
        return repr(self.__cells)

    def __str__(self) -> str:
        return str(self.__cells)

    def is_empty(self, row: List[Optional[str]] = None, index: int = None) -> bool:
        if index is not None:
            row = self[index]

        return all(cell is None for cell in row)

    def is_full(self, row: List[Optional[str]] = None, index: int = None) -> bool:
        if index is not None:
            row = self[index]

        return all(cell is not None for cell in row)

    def clear_rows(self) -> int:
        cleared_rows = []
        for i, row in enumerate(self):
            if self.is_full(row):
                cleared_rows.append(i)
                self[i].clear()

        if cleared_rows:
            # Drops all floating rows, going in descending order.
            # from the row above the bottommost cleared row, to the top of the board.
            for row in range(cleared_rows[-1] - 1, 0, -1):
                if self.is_empty(index=row):
                    continue

                cur_row = row
                while self.is_empty(index=cur_row + 1):
                    self[cur_row + 1], self[cur_row] = self[cur_row], self[cur_row + 1]
                    cur_row += 1

        return len(cleared_rows)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height
