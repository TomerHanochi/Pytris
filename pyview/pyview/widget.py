from typing import Union

import pygame as pg

from pyview.surface import Surface


class Widget(Surface):
    def __init__(self, x: float, y: float, width: float = None, height: float = None,
                 surface: Union[pg.Surface, Surface] = None, centered: bool = False) -> None:
        super().__init__(width, height, surface.image if isinstance(surface, Surface) else surface)

        self.x = x
        self.y = y
        if centered:
            self.x -= self.width * .5
            self.y -= self.height * .5

    def overlap(self, x: float, y: float) -> bool:
        return 0 <= x - self.x <= self.width and 0 <= y - self.y <= self.height

    @property
    def right(self) -> float:
        """ Returns the right index in the current rotation. """
        return self.x + self.width

    @property
    def left(self) -> float:
        """ Returns the left index in the current rotation. """
        return self.x

    @property
    def top(self) -> float:
        """ Returns the top index in the current rotation. """
        return self.y

    @property
    def bottom(self) -> float:
        """ Returns the bottom index in the current rotation. """
        return self.y + self.height
