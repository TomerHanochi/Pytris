from pyview.key import Key
from pyview.screen import Screen


class MainMenu(Screen):
    def __init__(self) -> None:
        super().__init__(600, 600)

    def key_down(self, key: Key) -> None:
        if key is key.SPACE:
            self.redirect('Game')
