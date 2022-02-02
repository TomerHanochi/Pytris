import pygame as pg

from classproperty import classproperty
from pyview.key import Key
from pyview.surface import Surface

SCREEN_REDIRECT = pg.event.custom_type()


class Screen(Surface):
    def __init__(self, width: int, height: int, fps: int = 60) -> None:
        super().__init__(width, height, pg.Surface((width, height)))
        self.fps = fps
        self.fps_clock = pg.time.Clock()

    @staticmethod
    def redirect(screen_id: str) -> None:
        """ Posts pygame event to redirect the user to the screen mapped to the screen id. """
        event = pg.event.Event(SCREEN_REDIRECT, screen_id=screen_id)
        pg.event.post(event)

    def set_as_main(self) -> None:
        self.image = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.id)

    def clock(self) -> None:
        """ Clocks screen to make sure it runs on a stable fps. """
        self.fps_clock.tick(self.fps)

    def update(self) -> None:
        """ Updates screen every frame. """
        ...

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

    @classproperty
    def id(cls) -> str:
        return cls.__name__
