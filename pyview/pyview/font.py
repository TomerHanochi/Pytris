from typing import Tuple

from pygame.freetype import Font as FreeTypeFont

from pyview.surface import Surface


class Font:
    def __init__(self, filepath: str) -> None:
        self.font = FreeTypeFont(filepath)

    def render(self, text: str, color: Tuple[int, int, int], size: int) -> Surface:
        return Surface(image=self.font.render(text, fgcolor=color, size=size)[0])
