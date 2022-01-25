import os
from pathlib import Path

import pygame as pg


class Assets:
    def __init__(self, dir_path: Path) -> None:
        for root, _, files in os.walk(dir_path):
            for file in files:
                path = Path(os.path.join(root, file))
                if path.suffix in {'.jpg', '.jpeg', '.png'}:
                    asset = pg.image.load(path).convert_alpha()
                elif path.suffix in {'.ttf', '.otf'}:
                    asset = pg.freetype.Font(path)
                elif path.suffix in {'.wav', '.ogg'}:
                    asset = pg.mixer.Sound(path)
                else:
                    continue

                setattr(self, path.stem, asset)
