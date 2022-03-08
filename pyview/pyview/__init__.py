import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['PYGAME_FREETYPE'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

from pygame import display

display.init()
info = display.Info()
DISPLAY_WIDTH, DISPLAY_HEIGHT = info.current_w, info.current_h
