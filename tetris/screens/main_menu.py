from functools import cached_property

from pyview.screen import Screen
from pyview.widget import Widget
from tetris.assets import Colors, Fonts


class MainMenu(Screen):
    def __init__(self) -> None:
        super().__init__(600, 600)

    def update(self) -> None:
        self.blit_widget(self.title)
        self.blit_widget(self.start_button)
        self.blit_widget(self.instructions_button)
        self.blit_widget(self.controls_button)

    def mouse_down(self, x: float, y: float) -> None:
        if self.start_button.overlap(x, y):
            self.redirect('Game')
        elif self.instructions_button.overlap(x, y):
            self.redirect('Instructions')
        elif self.controls_button.overlap(x, y):
            self.redirect('Controls')

    @property
    def spacing(self) -> float:
        return self.height * .05

    @cached_property
    def title(self) -> Widget:
        text = Fonts.pixel.render('TETRIS', Colors.white, self.height * .35)
        return Widget(x=self.width * .5,
                      y=self.height * .2 + text.height * .5,
                      surface=text, centered=True)

    @cached_property
    def start_button(self) -> Widget:
        text = Fonts.pixel.render('START', Colors.black, self.height * .15, background=Colors.white)
        return Widget(x=self.title.left + (self.title.width - text.width) * .5,
                      y=self.title.bottom + self.spacing,
                      surface=text)

    @cached_property
    def instructions_button(self) -> Widget:
        text = Fonts.pixel.render('INSTRUCTIONS', Colors.black, self.height * .15, background=Colors.white)
        return Widget(x=self.title.left + (self.title.width - text.width) * .5,
                      y=self.start_button.bottom + self.spacing,
                      surface=text)

    @cached_property
    def controls_button(self) -> Widget:
        text = Fonts.pixel.render('CONTROLS', Colors.black, self.height * .15, background=Colors.white)
        return Widget(x=self.title.left + (self.title.width - text.width) * .5,
                      y=self.instructions_button.bottom + self.spacing,
                      surface=text)
