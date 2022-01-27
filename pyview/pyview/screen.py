from dataclasses import dataclass, field
from typing import ClassVar

import pygame as pg

from pyview.key import Key
from pyview.widget import Widget

SCREEN_REDIRECT = pg.event.custom_type()


@dataclass(frozen=True)
class Screen:
    ID: ClassVar[str] = None

    width: int
    height: int
    caption: str
    fps: int = 60
    fps_clock: pg.time.Clock = field(init=False, default_factory=pg.time.Clock)

    def __init_subclass__(cls, **kwargs) -> None:
        if not isinstance(cls.ID, str):
            raise ValueError(f'{cls.__name__} - ID must be set on child class and be a string')

    @staticmethod
    def redirect(screen_id: str) -> None:
        """ Posts pygame event to redirect the user to the screen mapped to the screen id. """
        event = pg.event.Event(SCREEN_REDIRECT, screen_id=screen_id)
        pg.event.post(event)

    def update(self) -> None:
        """ Updates screen every frame. """
        pass

    def set_as_main(self) -> None:
        """ Resets screen as main screen. """
        pg.display.quit()
        pg.display.init()
        pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.caption)

    def clock(self) -> None:
        """ Clocks screen to make sure it runs on a stable fps. """
        self.fps_clock.tick(self.fps)

    def blit(self, widget: Widget) -> None:
        """ Draws a drawable_object on the screen with the specified coordinates. """
        self.window.blit(widget.surface, (widget.x, widget.y))

    def fill(self, color: tuple, x: float = 0, y: float = 0, width: float = None,
             height: float = None, centered: bool = False) -> None:
        """ Colors a specified portion of the screen with the given Color. """
        if centered:
            x -= width * .5
            y -= height * .5

        self.window.fill(rect=(x, y, width or self.width - x, height or self.height - y),
                         color=color)

    def quit(self) -> None:
        """ Gets called when program exits. """
        ...

    def key_down(self, key: Key) -> None:
        """ Gets called when key is pressed. """
        ...

    def key_up(self, key: Key) -> None:
        """ Gets called when key is lifted. """
        ...

    def mouse_down(self, x: float, y: float) -> None:
        """ Gets called when mouse is pressed. """
        ...

    def mouse_up(self, x: float, y: float) -> None:
        """ Gets called when mouse is lifted. """
        ...

    def mouse_wheel(self, x: float, y: float, dx: float, dy: float) -> None:
        """ Gets called when mouse wheel is used. """
        ...

    def mouse_move(self, x: float, y: float, dx: float, dy: float) -> None:
        """ Gets called when mouse is moved. """
        ...

    @property
    def window(self) -> pg.Surface:
        return pg.display.get_surface()
