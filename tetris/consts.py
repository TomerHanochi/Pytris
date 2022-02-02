import os
from pathlib import Path
from typing import Tuple

from classproperty import classproperty


class Consts:
    @classproperty
    def base_path(cls) -> str:
        return str(Path(__file__).parent)

    @classproperty
    def assets_directory(cls) -> str:
        return os.path.join(cls.base_path, 'assets')

    @classproperty
    def images_directory(cls) -> str:
        return os.path.join(cls.assets_directory, 'images')

    @classproperty
    def fonts_directory(cls) -> str:
        return os.path.join(cls.assets_directory, 'fonts')

    @classproperty
    def sounds_directory(cls) -> str:
        return os.path.join(cls.assets_directory, 'sounds')

    @classproperty
    def display_width(cls) -> int:
        return 1920

    @classproperty
    def display_height(cls) -> int:
        return 1080

    @classproperty
    def display_size(cls) -> Tuple[int, int]:
        return cls.display_width, cls.display_height
