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
            self.x -= self.width
            self.y -= self.height

    def overlap(self, x: float, y: float) -> bool:
        return 0 <= x - self.x <= self.width and 0 <= y - self.y <= self.height

    def blit(self, widget: 'Widget') -> None:
        self.blit_surface(widget.surface, widget.x, widget.y)

    def blit_surface(self, surface: pg.Surface, x: float, y: float) -> None:
        self.surface.blit(surface, (x, y))

    def fill(self, color: tuple, x: float = 0, y: float = 0, width: float = None,
             height: float = None, centered: bool = False) -> None:
        if centered:
            x -= width * .5
            y -= height * .5

        self.surface.fill(rect=(x, y, width or self.width - x, height or self.height - y),
                          color=color)

    @property
    def width(self) -> int:
        return self.surface.get_width()

    @property
    def height(self) -> int:
        return self.surface.get_height()
