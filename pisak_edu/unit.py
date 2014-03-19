from gi.repository import Gdk

SCREEN_DPMM = Gdk.Screen.width() / float(Gdk.Screen.width_mm())
SCREEN_DPI = SCREEN_DPMM * 25.4

def mm(value):
    return int(value * SCREEN_DPMM)
