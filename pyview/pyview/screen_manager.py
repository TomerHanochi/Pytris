import ast
import importlib.util
import os
from _ast import ClassDef
from functools import cached_property
from pathlib import Path
from typing import List

import pygame as pg

from pyview.key import Key
from pyview.screen import SCREEN_REDIRECT, Screen


class ScreenManager:
    def __init__(self, screen_id: str, screen_dir: str) -> None:
        pg.init()
        pg.display.set_mode((1, 1))

        self.run = True
        self.screens = {screen.id: screen for screen in self.import_screens(screen_dir)}
        self.current_screen_id = screen_id
        self.set_display()

    def __enter__(self) -> 'ScreenManager':
        return self

    def __exit__(self, error_type: BaseException, value: str, traceback: str) -> bool:
        self.current_screen.quit()
        pg.quit()
        if error_type is KeyboardInterrupt:
            return True

    def set_display(self) -> None:
        """ Sets screen as main screen. """
        pg.display.set_mode(self.current_screen.size)
        pg.display.set_caption(self.current_screen.id)

    def handle_event(self, event: pg.event.Event) -> None:
        """ Handles all allowed event types. """
        if event.type == pg.QUIT:
            self.run = False
        elif event.type == pg.KEYDOWN:
            if Key.has_value(event.key):
                self.current_screen.key_down(Key(event.key))
        elif event.type == pg.KEYUP:
            if Key.has_value(event.key):
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
        elif event.type == SCREEN_REDIRECT:
            self.current_screen_id = event.screen_id
            self.set_display()

    def handle_events(self) -> None:
        """ Loops over all events in queue and handles them. """
        for event in pg.event.get():
            self.handle_event(event)

    def execute(self) -> None:
        """ Execution of a single frame. """
        self.handle_events()
        self.current_screen.update()
        self.current_screen.clock()
        self.window.blit(self.current_screen.image, (0, 0))
        pg.display.update()

    def main_loop(self) -> None:
        while self.run:
            self.execute()

    @cached_property
    def window(self) -> pg.Surface:
        return pg.display.get_surface()

    @property
    def current_screen(self) -> Screen:
        return self.screens[self.current_screen_id]

    @staticmethod
    def import_screens(screen_dir: str) -> List[Screen]:
        """ Returns a list of all screens in the given directory. """
        screens = []
        for root, _, files in os.walk(screen_dir):
            for filename in files:
                path = Path(os.path.join(root, filename))

                if path.suffix != '.py':
                    continue

                with open(path) as f:
                    module = ast.parse(f.read())
                    for class_definition in module.body:
                        # if the child is not a class definition, or it's not inheriting from Screen
                        if not isinstance(class_definition, ClassDef) or class_definition.bases[0].id != 'Screen':
                            continue

                        spec = importlib.util.spec_from_file_location(path.stem, path)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        cls = getattr(module, class_definition.name)
                        screens.append(cls())
        return screens
