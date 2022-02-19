from typing import Tuple

from pygame.freetype import Font as FreeTypeFont

from pyview.surface import Surface


class Font:
    def __init__(self, filepath: str) -> None:
        self.font = FreeTypeFont(filepath)

    def render(self, text: str, color: Tuple[int, int, int], size: int, background: Tuple[int, int, int] = None) -> Surface:
        rendered_text = Surface(image=self.font.render(text, fgcolor=color, size=size)[0])
        if background is None:
            return rendered_text

        offset = 0.075
        tmp = Surface(rendered_text.width * (1 + offset * 2), rendered_text.height * (1 + offset * 2))
        tmp.fill(background)
        tmp.blit(rendered_text, rendered_text.width * offset, rendered_text.height * offset)
        return tmp
