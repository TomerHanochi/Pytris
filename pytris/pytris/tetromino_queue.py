from random import shuffle

from pytris.tetromino import Tetromino, NAMES


class TetrominoQueue:
    def __init__(self) -> None:
        self.__queue = []

    def __getitem__(self, index: int) -> str:
        return self.__queue[index]

    def __len__(self) -> int:
        return len(self.__queue)

    def __repr__(self) -> str:
        return repr(self.__queue)

    def update(self) -> None:
        bag = NAMES.copy()
        shuffle(bag)
        self.__queue.extend(Tetromino(name) for name in bag)

    def pop(self) -> Tetromino:
        return self.__queue.pop(0)
