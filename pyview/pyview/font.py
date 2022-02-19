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

        offset = rendered_text.height * 0.1
        tmp = Surface(rendered_text.width + offset * 2, rendered_text.height + offset * 2)
        tmp.fill(background)
        tmp.blit(rendered_text, offset, offset)
        return tmp
