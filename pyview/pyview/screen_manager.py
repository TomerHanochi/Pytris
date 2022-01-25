from dataclasses import dataclass
from typing import Dict

import pygame as pg

from pyview.key import Key
from pyview.screen import Screen


@dataclass
class ScreenManager:
    screen_id: str
    screens: Dict[str, Screen]

    def __post_init__(self) -> None:
        self.current_screen.set_as_main()

    def handle_event(self, event: pg.event.Event) -> None:
        """ Handles all allowed event types. """
        if event.type == pg.QUIT:
            self.current_screen.quit()
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            self.current_screen.key_down(Key(event.key))
        elif event.type == pg.KEYUP:
            self.current_screen.key_up(Key(event.key))
        elif event.type == pg.MOUSEBUTTONDOWN:
            if 1 <= event.button <= 3:
                self.current_screen.mouse_down(*pg.mouse.get_pos())
        elif event.type == pg.MOUSEBUTTONUP:
            if 1 <= event.button <= 3:
                self.current_screen.mouse_up(*pg.mouse.get_pos())
        elif event.type == pg.MOUSEWHEEL:
            self.current_screen.mouse_wheel(*pg.mouse.get_pos(), event.x, event.y)
        elif event.type == pg.MOUSEMOTION:
            self.current_screen.mouse_move(*pg.mouse.get_pos(), *event.rel)
        elif event.type == Screen.REDIRECT:
            self.screen_id = event.screen_id
            self.current_screen.set_as_main()

    def handle_events(self) -> None:
        """ Loops over all events in queue and handles them. """
        for event in pg.event.get():
            self.handle_event(event)

    def execute(self) -> None:
        """ Execution of a single frame. """
        self.handle_events()
        self.current_screen.update()
        self.current_screen.clock()
        pg.display.update()

    @property
    def current_screen(self) -> Screen:
        """ Returns the current screen. """
        return self.screens[self.screen_id]
