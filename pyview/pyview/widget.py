from dataclasses import dataclass

import pygame as pg


@dataclass
class Widget:
    surface: pg.Surface
    x: float
    y: float
    centered: bool = False

    def __post_init__(self) -> None:
        if self.centered:
            self.x -= self.w
            self.y -= self.h

    def overlap(self, x: float, y: float) -> bool:
        return 0 <= x - self.x <= self.w and 0 <= y - self.y <= self.h

    @property
    def w(self) -> int:
        return self.surface.get_width()

    @property
    def h(self) -> int:
        return self.surface.get_height()
