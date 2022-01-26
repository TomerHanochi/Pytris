from typing import Generic, Iterator, TypeVar

T = TypeVar('T')


class Array(Generic[T]):
    def __init__(self, iterator: Iterator[T]) -> None:
        self.__values = list(iterator)

    def __getitem__(self, index: int) -> T:
        return self.__values[index]

    def __setitem__(self, index: int, value: T) -> None:
        self.__values[index] = value

    def __iter__(self) -> Iterator[T]:
        return iter(self.__values)

    def __len__(self) -> int:
        return len(self.__values)

    def __repr__(self) -> str:
        return repr(self.__values)

    def __str__(self) -> str:
        return str(self.__values)

    def clear(self) -> None:
        self.__init__(None for _ in self)


class Queue(Generic[T]):
    def __init__(self, iterator: Iterator[T]) -> None:
        self.__values = list(iterator)

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
