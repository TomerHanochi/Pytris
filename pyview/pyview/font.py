from typing import Literal, Tuple

from pygame.freetype import Font as FreeTypeFont

from pyview.surface import Surface

LTR = 'ltr'
RTL = 'rtl'
CENTER = 'center'


class Font:
    def __init__(self, filepath: str) -> None:
        self.font = FreeTypeFont(filepath)

    def render(self, text: str, color: Tuple[int, int, int], size: int, background: Tuple[int, int, int] = None,
               align: Literal['ltr', 'rtl', 'center'] = CENTER, spacing: int = 0) -> Surface:
        split_text = text.split('\n')
        rendered_split_text = [Surface(image=self.font.render(line, fgcolor=color, size=size * 2)[0]) for line in split_text]
        rendered_text = Surface(width=max(line.width for line in rendered_split_text),
                                height=len(rendered_split_text) * (size + spacing) - spacing)
        for i, line in enumerate(rendered_split_text):
            if align == LTR:
                x = 0
            elif align == RTL:
                x = rendered_text.width - line.width
            elif align == CENTER:
                x = (rendered_text.width - line.width) * .5
            else:
                raise ValueError('align must be one of \'ltr\', \'rtl\' or \'center\'')

            rendered_text.blit(line, x, i * (size + spacing))

        if background is None:
            return rendered_text

        offset = size * 0.1
        background_surface = Surface(rendered_text.width + offset * 2, rendered_text.height + offset * 2)
        background_surface.fill(background)
        background_surface.blit(rendered_text, offset, offset)
        return background_surface
