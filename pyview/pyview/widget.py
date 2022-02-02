from pyview.surface import Surface


class Widget(Surface):
    def __init__(self, surface: Surface, x: float, y: float, centered: bool = False) -> None:
        super().__init__(surface.image.copy(), surface.width, surface.height)

        self.x = x
        self.y = y
        if centered:
            self.x -= self.width
            self.y -= self.height

    def overlap(self, x: float, y: float) -> bool:
        return 0 <= x - self.x <= self.width and 0 <= y - self.y <= self.height
