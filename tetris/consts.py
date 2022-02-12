import os
from pathlib import Path


class Consts:
    base_path = str(Path(__file__).parent)
    assets_directory = os.path.join(base_path, 'assets')
    images_directory = os.path.join(assets_directory, 'images')
    fonts_directory = os.path.join(assets_directory, 'fonts')
    sounds_directory = os.path.join(assets_directory, 'sounds')

    board_width = 10
    board_height = 20
    block_size = 40

    next_size = 6
