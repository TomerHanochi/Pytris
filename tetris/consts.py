import os
from pathlib import Path

from pyview.utils.class_property import classproperty


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
