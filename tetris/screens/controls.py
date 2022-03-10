from functools import cached_property

from pyview.screen import Screen
from pyview.widget import Widget
from tetris.assets import Colors, Fonts, Images

CONTROLS = """Right Arrow moves right
Left Arrow Moves Left
Space Bar to hard drop
Down Arrow to soft drop
Up Arrow or X to rotate right
Ctrl or Z to rotate left
Shift or C to hold
Escape or F1 to pause"""


class Controls(Screen):
    def __init__(self) -> None:
        super().__init__(700, 500, fps=30)

    def update(self) -> None:
        self.fill(Colors.black)
        self.blit_widget(self.title)
        self.blit_widget(self.controls)
        self.blit_widget(self.back)

    def mouse_down(self, x: float, y: float) -> None:
        if self.back.overlap(x, y):
            self.redirect('MainMenu')

    @cached_property
    def title(self) -> Widget:
        return Widget(x=self.width * .5, y=self.height * 0.075, centered=True,
                      surface=Fonts.pixel.render('Controls', Colors.white, self.height * 0.1))

    @cached_property
    def back(self) -> Widget:
        return Widget(x=self.width * 0.01, y=self.title.y, surface=Images.back)

    @cached_property
    def controls(self) -> Widget:
        return Widget(x=self.width * 0.03125, y=self.title.bottom + self.height * 0.025,
                      surface=Fonts.pixel.render(CONTROLS, Colors.white, self.height * 0.05, align='ltr', spacing=15))
