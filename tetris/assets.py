import os
from typing import Any

from pyview.font import Font
from pyview.surface import Surface
from tetris.consts import Consts


class AssetsMeta(type):
    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except KeyError:
            raise AttributeError(f'No asset named {key}')


class Assets(metaclass=AssetsMeta):
    pass


class Fonts(Assets):
    pixel = Font(os.path.join(Consts.fonts_directory, 'pixelboy.ttf'))


class Colors(Assets):
    transparent = (0, 0, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)


class Images(Assets):
    O = Surface.load(os.path.join(Consts.images_directory, 'O.png'), Consts.block_size, Consts.block_size)
    I = Surface.load(os.path.join(Consts.images_directory, 'I.png'), Consts.block_size, Consts.block_size)
    T = Surface.load(os.path.join(Consts.images_directory, 'T.png'), Consts.block_size, Consts.block_size)
    L = Surface.load(os.path.join(Consts.images_directory, 'L.png'), Consts.block_size, Consts.block_size)
    J = Surface.load(os.path.join(Consts.images_directory, 'J.png'), Consts.block_size, Consts.block_size)
    S = Surface.load(os.path.join(Consts.images_directory, 'S.png'), Consts.block_size, Consts.block_size)
    Z = Surface.load(os.path.join(Consts.images_directory, 'Z.png'), Consts.block_size, Consts.block_size)
    border = Surface.load(os.path.join(Consts.images_directory, 'border.png'), Consts.block_size, Consts.block_size)
    ghost = Surface.load(os.path.join(Consts.images_directory, 'ghost.png'), Consts.block_size, Consts.block_size)


class Sounds(Assets):
    pass
