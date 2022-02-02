from typing import Dict, Tuple, TypeVar, Union

from pygame.font import Font
from pygame.mixer import Sound

from pyview.surface import Surface

AssetType = TypeVar('AssetType', Surface, Font, Sound, Union[Tuple[int, int, int], Tuple[int, int, int, int]])


class Assets(Dict[str, AssetType]):
    def __getattr__(self, key: str) -> AssetType:
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f'No asset named {key}')
