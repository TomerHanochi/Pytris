from random import shuffle

from pytris.tetromino import Tetromino


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
        bag = list(Tetromino.rotations.keys())
        shuffle(bag)
        self.__queue.extend(bag)

    def pop(self) -> str:
        return self.__queue.pop(0)
