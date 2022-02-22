from functools import cached_property

from pyview.key import Key
from pyview.screen import Screen
from pyview.widget import Widget
from tetris.assets import Colors, Fonts

INSTRUCTIONS = """The aim in Tetris is simple;
you bring down blocks from the top
of the screen. You can move the
blocks around, either left to right
in addition to rotating them.

The blocks fall at a certain
rate, but you can make them fall
faster if you’re sure of your
positioning.

Your objective is to get all
the blocks to fill all the empty
space in a line at the bottom of
the screen; whenever you do this,
you’ll find that the blocks vanish
and you get awarded some points."""


class Instructions(Screen):
    def __init__(self) -> None:
        super().__init__(800, 800, fps=5)

    def update(self) -> None:
        self.fill(Colors.black)
        self.blit_widget(self.title)
        self.blit_widget(self.instructions)

    def key_down(self, key: Key) -> None:
        if key is Key.ESCAPE:
            self.redirect('MainMenu')

    @cached_property
    def title(self) -> Widget:
        return Widget(x=self.width * .5,
                      y=self.height * 0.075,
                      surface=Fonts.pixel.render('INSTRUCTIONS', Colors.white, self.height * 0.075),
                      centered=True)

    @cached_property
    def instructions(self) -> Widget:
        return Widget(x=25,
                      y=self.title.bottom + 20,
                      surface=Fonts.pixel.render(INSTRUCTIONS, Colors.white, 26, align='ltr', spacing=15))
