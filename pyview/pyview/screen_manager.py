import ast
import importlib.util
import os
from _ast import ClassDef
from typing import List

import pygame as pg

from pyview.key import Key
from pyview.screen import SCREEN_REDIRECT, Screen


class ScreenManager:
    def __init__(self, screen_id: str, screen_dir: str) -> None:
        self.screen_id = screen_id
        self.run = True
        self.screens = {screen.id: screen for screen in self.import_screens(screen_dir)}
        self.current_screen.set_as_main()

    def __enter__(self) -> 'ScreenManager':
        pg.init()
        return self

    def __exit__(self, type, value, traceback) -> bool:
        self.current_screen.quit()
        pg.quit()
        if type is KeyboardInterrupt:
            return True

    def handle_event(self, event: pg.event.Event) -> None:
        """ Handles all allowed event types. """
        if event.type == pg.QUIT:
            self.run = False
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
        elif event.type == SCREEN_REDIRECT:
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

    def main_loop(self) -> None:
        while self.run:
            self.execute()

    @property
    def current_screen(self) -> Screen:
        """ Returns the current screen. """
        return self.screens[self.screen_id]

    @staticmethod
    def import_screens(screen_dir: str) -> List[Screen]:
        """ Returns a list of all screens in the given directory. """
        screens = []
        for root, _, files in os.walk(screen_dir):
            for filename in files:
                if not filename.endswith('.py'):
                    continue

                full_path = os.path.join(root, filename)
                with open(full_path) as f:
                    node = ast.parse(f.read())
                    for cls_def in node.body:
                        # if the child is not a class definition, or it's not inheriting from Screen
                        if not isinstance(cls_def, ClassDef) or cls_def.bases[0].id != 'Screen':
                            continue

                        spec = importlib.util.spec_from_file_location(filename[:-3], full_path)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        cls = getattr(module, cls_def.name)
                        screens.append(cls())
        return screens
