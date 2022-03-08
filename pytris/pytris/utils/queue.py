from typing import Generic, Iterator, TypeVar

T = TypeVar('T')


class Queue(Generic[T]):
    def __init__(self, iterator: Iterator[T] = None) -> None:
        self.__values = list(iterator) if iterator is not None else []

    def __getitem__(self, index: int) -> T:
        return self.__values[index]

    def __len__(self) -> int:
        return len(self.__values)

    def __repr__(self) -> str:
        return repr(self.__values)

    def __str__(self) -> str:
        return str(self.__values)

    def insert(self, item: T) -> None:
        self.__values.append(item)

    def pop(self) -> T:
        return self.__values.pop(0)
