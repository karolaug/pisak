from subprocess import Popen, PIPE
from collections import namedtuple
from gi.repository import Gdk
import re
from sys import platform

temp = []
screen_mm = namedtuple('ScreenSizeMM', 'width height')
screen_pixels = namedtuple('ScreenSizePix', 'width height')
size_pix = screen_pixels(Gdk.Screen.width(), Gdk.Screen.height())


if 'linux' in platform:
    try:
        out = str(Popen('xrandr', stdout=PIPE).stdout.read()).split()
        for mm in out:
            if 'mm' in mm:
                mm = re.sub('[^0-9]', '', mm)
                temp.append(mm)
                if len(temp) == 2:
                    size_mm = screen_mm(int(temp[0]), int(temp[1]))
                    break
    except OSError:
        print('No xrandr, falling back to Gdk for screen size in mm.')
        size_mm = screen_mm(Gdk.Screen.width_mm(), Gdk.Screen.height_mm())
else:
    print('Apparently not on linux, using Gdk.Screen for mm size.')
    size_mm = screen_mm(Gdk.Screen.width_mm(), Gdk.Screen.height_mm())

try:
    SCREEN_DPMM = getattr(size_pix, 'width') / getattr(size_mm, 'width')
except ZeroDivisionError:
    print('Issue with xrandr causes screen size to be 0mm, using Gdk.Screen of mm size.')
    size_mm = screen_mm(Gdk.Screen.width_mm(), Gdk.Screen.height_mm())
    SCREEN_DPMM = getattr(size_pix, 'width') / getattr(size_mm, 'width')

SCREEN_DPI = SCREEN_DPMM * 25.4


def mm(value):
    return int(value * SCREEN_DPMM)

def w(v):
    return v * Gdk.Screen.width()

def h(v):
    return v * Gdk.Screen.height()

def pt_to_px(pt):
    return pt * SCREEN_DPMM

if __name__ == '__main__':
    msg = 'Your screen size in mm is {} x {}, in pixels {} x {} which gives {} DPI.'
    print(msg.format(getattr(size_mm, 'width'), getattr(size_mm, 'height'),
                     getattr(size_pix, 'width'), getattr(size_pix, 'height'),
                     round(SCREEN_DPI)))
