from typing import Iterator, Optional, List


class Row:
    def __init__(self, width: int) -> None:
        self.__cells = [None for _ in range(width)]

    def __getitem__(self, index: int) -> Optional[str]:
        return self.__cells[index]

    def __setitem__(self, index: int, value: Optional[str]) -> None:
        self.__cells[index] = value

    def __iter__(self) -> Iterator[Optional[str]]:
        return iter(self.__cells)

    def __len__(self) -> int:
        return len(self.__cells)

    def __repr__(self) -> str:
        return repr(self.__cells)

    def __str__(self) -> str:
        return str(self.__cells)

    def clear(self) -> None:
        self.__init__(len(self))

    @property
    def is_empty(self) -> bool:
        return all(cell is None for cell in self)

    @property
    def is_full(self) -> bool:
        return all(cell is not None for cell in self)


class Board:
    def __init__(self, width: int, height: int) -> None:
        self.__cells = [Row(width) for _ in range(height)]

    def __getitem__(self, index: int) -> Row:
        return self.__cells[index]

    def __setitem__(self, index: int, value: Row) -> None:
        self.__cells[index] = value

    def __iter__(self) -> Iterator[Row]:
        return iter(self.__cells)

    def __len__(self) -> int:
        return len(self.__cells)

    def __repr__(self) -> str:
        return repr(self.__cells)

    def __str__(self) -> str:
        return str(self.__cells)

    def clear_rows(self) -> int:
        cleared_rows = []
        for i, row in enumerate(self):
            if row.is_full:
                cleared_rows.append(i)
                self[i].clear()

        if cleared_rows:
            # Drops all floating rows, going in descending order.
            # from the row above the bottommost cleared row, to the top of the board.
            for row in range(cleared_rows[-1] - 1, 0, -1):
                if self[row].is_empty:
                    continue

                cur_row = row
                while self[cur_row + 1].is_empty:
                    self[cur_row + 1] = self[cur_row]
                    self[cur_row].clear()
                    cur_row += 1

        return len(cleared_rows)
