import os

from pyview.screen_manager import ScreenManager


def main() -> None:
    screen_dir = os.path.join(os.path.dirname(__file__), 'screens')
    with ScreenManager('MainMenu', screen_dir) as manager:
        manager.main_loop()


if __name__ == '__main__':
    main()
