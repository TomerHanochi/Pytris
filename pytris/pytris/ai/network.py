from dataclasses import dataclass, field
from functools import cached_property
from random import uniform
from uuid import UUID, uuid4

from pytris.utils.vector import Vector


@dataclass(frozen=True)
class Network:
    id: UUID = field(default_factory=uuid4, init=False)
    weights: Vector = field(hash=False)

    def __post_init__(self) -> None:
        self.weights.normalize()

    def mutate(self, power: float) -> None:
        self.weights.__iadd__(uniform(-power, power) for _ in range(self.size))
        self.weights.normalize()

    @cached_property
    def size(self) -> int:
        return len(self.weights)

    @classmethod
    def random(cls, size: int) -> 'Network':
        return cls(Vector.random(size))
