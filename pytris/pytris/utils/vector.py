import math
from collections.abc import Iterable
from functools import partialmethod
from operator import add, floordiv, iadd, ifloordiv, imul, isub, itruediv, mul, sub, truediv
from random import uniform
from typing import Callable, Iterable as IterableType, Union

from pytris.utils.array import Array

Operand = Union[IterableType[float], float]
VectorOperator = Callable[[Operand], 'Vector']


class Vector(Array[float]):
    def operator(self, other: Operand, operator: Callable[[float, float], float]) -> 'Vector':
        """
        Generic function for performing an operation on each of the Vector's elements.
        :param other: an Iterable of type float or a type float object.
        :param operator: a function to perform on each element of the Vector.
        :return: a new Vector with the altered values.
        """
        if isinstance(other, Iterable):
            return Vector(operator(a, b) for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            return Vector(operator(a, other) for a in self)
        else:
            raise ValueError(f'Can\'t {operator.__name__} objects of type Vector and {other.__class__.__name__}')

    def ioperator(self, other: Operand, operator: Callable[[float, float], float]) -> 'Vector':
        """
        Generic function for performing an in place operation on each of the Vector's elements.
        :param other: an Iterable of type float or a type float object.
        :param operator: a function to perform on each element of the Vector.
        """
        if isinstance(other, Iterable):
            for i, (a, b) in enumerate(zip(self, other)):
                self[i] = operator(a, b)
        elif isinstance(other, (int, float)):
            for i, a in enumerate(self):
                self[i] = operator(a, other)
        else:
            raise ValueError(f'Can\'t {operator.__name__} objects of type Vector and {other.__class__.__name__}')
        return self

    def dot(self, other: IterableType[float]) -> float:
        if isinstance(other, Iterable):
            return sum(a * b for a, b in zip(self, other))
        raise ValueError(f'Can\'t dot product objects of type Vector and {other.__class__.__name__}')

    def normalize(self) -> None:
        self.magnitude = 1

    @property
    def magnitude(self) -> float:
        return math.sqrt(sum(a * a for a in self))

    @magnitude.setter
    def magnitude(self, magnitude: float) -> None:
        self.__imul__(magnitude / self.magnitude)

    @classmethod
    def random(cls, size: int, magnitude: float = 1) -> 'Vector':
        """ Creates a random vector with 'size' elements, and magnitude of 'magnitude'. """
        vector = cls(uniform(-1, 1) for _ in range(size))
        vector.magnitude = magnitude
        return vector

    def __str__(self) -> str:
        return '(' + super().__str__()[1:-1] + ')'

    def __repr__(self) -> str:
        return f'Vector({self!s})'

    __add__: VectorOperator = partialmethod(operator, operator=add)
    __iadd__: VectorOperator = partialmethod(ioperator, operator=iadd)
    __sub__: VectorOperator = partialmethod(operator, operator=sub)
    __isub__: VectorOperator = partialmethod(ioperator, operator=isub)
    __mul__: VectorOperator = partialmethod(operator, operator=mul)
    __imul__: VectorOperator = partialmethod(ioperator, operator=imul)
    __truediv__: VectorOperator = partialmethod(operator, operator=truediv)
    __itruediv__: VectorOperator = partialmethod(ioperator, operator=itruediv)
    __floordiv__: VectorOperator = partialmethod(operator, operator=floordiv)
    __ifloordiv__: VectorOperator = partialmethod(ioperator, operator=ifloordiv)
