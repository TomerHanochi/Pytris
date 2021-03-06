from dataclasses import dataclass
from random import shuffle
from typing import Any, Dict, List

from pytris.tetromino import NAMES, Tetromino
from pytris.utils.queue import Queue


@dataclass
class TetrominoQueue(Queue[Tetromino]):
    def __init__(self) -> None:
        super().__init__()

    def update(self) -> None:
        bag = NAMES.copy()
        shuffle(bag)
        for name in bag:
            self.insert(Tetromino(name))

    def to_json(self) -> List[Dict[str, Any]]:
        return [tetromino.to_json() for tetromino in self]
