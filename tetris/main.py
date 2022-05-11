import sys
import os
from pathlib import Path

from pyview.screen_manager import ScreenManager


def main() -> None:
    # Needed to import screens
    cur_dir = Path(__file__).parent
    sys.path.append(str(cur_dir.parent))

    screen_dir = os.path.join(cur_dir, 'screens')
    with ScreenManager('MainMenu', screen_dir) as manager:
        manager.main_loop()


if __name__ == '__main__':
    main()
