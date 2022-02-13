import os
from pathlib import Path

from pyview import DISPLAY_HEIGHT, DISPLAY_WIDTH


class Consts:
    base_path = str(Path(__file__).parent)
    assets_directory = os.path.join(base_path, 'assets')
    images_directory = os.path.join(assets_directory, 'images')
    fonts_directory = os.path.join(assets_directory, 'fonts')
    sounds_directory = os.path.join(assets_directory, 'sounds')

    display_width = DISPLAY_WIDTH
    display_height = DISPLAY_HEIGHT

    game_screen_width = DISPLAY_HEIGHT
    game_screen_height = DISPLAY_HEIGHT * .75

    board_width = 10
    board_height = 20
    # the board border should be 80 percent of the screen height
    block_size = game_screen_height * 0.8 // (board_height + 2)

    next_size = 6
