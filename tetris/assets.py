import os
from typing import Tuple, Type, TypeVar, Union

from pygame.font import Font
from pygame.mixer import Sound

from pyview.surface import Surface
from tetris.consts import Consts

AssetType = TypeVar('AssetType', Surface, Font, Sound, Union[Tuple[int, int, int], Tuple[int, int, int, int]])


class Assets(Type[AssetType]):
    def __getitem__(cls, key: str) -> AssetType:
        try:
            return getattr(cls, key)
        except KeyError:
            raise AttributeError(f'No asset named {key}')


class Images(metaclass=Assets):
    O = Surface.load(os.path.join(Consts.images_directory, 'O.png'), Consts.block_size, Consts.block_size)
    I = Surface.load(os.path.join(Consts.images_directory, 'I.png'), Consts.block_size, Consts.block_size)
    T = Surface.load(os.path.join(Consts.images_directory, 'T.png'), Consts.block_size, Consts.block_size)
    L = Surface.load(os.path.join(Consts.images_directory, 'L.png'), Consts.block_size, Consts.block_size)
    J = Surface.load(os.path.join(Consts.images_directory, 'J.png'), Consts.block_size, Consts.block_size)
    S = Surface.load(os.path.join(Consts.images_directory, 'S.png'), Consts.block_size, Consts.block_size)
    Z = Surface.load(os.path.join(Consts.images_directory, 'Z.png'), Consts.block_size, Consts.block_size)
    border = Surface.load(os.path.join(Consts.images_directory, 'border.png'), Consts.block_size, Consts.block_size)
    ghost = Surface.load(os.path.join(Consts.images_directory, 'ghost.png'), Consts.block_size, Consts.block_size)


class Colors(metaclass=Assets):
    transparent = (0, 0, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)


class Fonts(metaclass=Assets):
    pass


class Sounds(metaclass=Assets):
    pass
