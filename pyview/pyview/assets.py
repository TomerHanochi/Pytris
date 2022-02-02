from typing import Dict, Generic, TypeVar

from pygame.font import Font
from pygame.mixer import Sound

from pyview.surface import Surface

AssetType = TypeVar('AssetType', Surface, Font, Sound)


class Assets(Generic[AssetType]):
    def __init__(self, assets: Dict[str, AssetType]) -> None:
        for attr, value in assets.items():
            setattr(self, attr, value)

    def __getitem__(self, key: str) -> AssetType:
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(f'No asset named {key}')
