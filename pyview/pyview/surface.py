from typing import Tuple

import pygame as pg


class Surface:
    def __init__(self, image: pg.Surface, width: float = None, height: float = None) -> None:
        self.image = pg.transform.smoothscale(image, (width or image.get_width(),
                                                      height or image.get_height())).convert_alpha()

    def blit(self, surface: 'Surface', x: float, y: float, centered: bool = False) -> None:
        if centered:
            x -= surface.width / 2
            y -= surface.height / 2

        self.image.blit(surface.image, (x, y))

    def fill(self, color: tuple, x: float = 0, y: float = 0, width: float = None,
             height: float = None, centered: bool = False) -> None:
        """ Colors a specified portion of the screen with the given Color. """
        if centered:
            x -= width * .5
            y -= height * .5

        self.image.fill(rect=(x, y, width or self.width - x, height or self.height - y),
                        color=color)

    @property
    def width(self) -> int:
        return self.image.get_width()

    @width.setter
    def width(self, width: float) -> None:
        self.image = pg.transform.smoothscale(self.image, (width, self.height))

    @property
    def height(self) -> int:
        return self.image.get_height()

    @height.setter
    def height(self, height: float) -> None:
        self.image = pg.transform.smoothscale(self.image, (self.width, height))

    @property
    def size(self) -> Tuple[int, int]:
        return self.image.get_size()

    @size.setter
    def size(self, size: Tuple[int, int]) -> None:
        self.image = pg.transform.smoothscale(self.image, size)

    @classmethod
    def load(cls, filename, width: float = None, height: float = None) -> 'Surface':
        return cls(pg.image.load(filename), width, height)
