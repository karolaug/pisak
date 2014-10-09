'''
ClutterScript paint specific signal handler library
'''
from gi.repository import Clutter

from pisak import signals


@signals.registered_handler("paint/set_color")
def set_color(easel, color):
    """
    Set easel line color
    """
    easel.rgba = _convert_color(color)


@signals.registered_handler("paint/set_line_width")
def set_line_width(easel, line_width):
    """
    Set easel line width
    """
    easel.line_width = int(line_width)


@signals.registered_handler("paint/clear_canvas")
def clear_canvas(easel):
    """
    Clear easel canvas
    """
    easel.clear_canvas()


@signals.registered_handler("paint/save_to_file")
def save_to_file(easel):
    """
    Save easel canvas picture to png file
    """
    easel.save_to_file()


@signals.registered_handler("paint/new_spot")
def new_spot(easel):
    """
    Localize new drawing spot
    """
    easel.run_localizer()


@signals.registered_handler("paint/navigate")
def navigate(easel):
    """
    Back to drawing and navigate
    """
    easel.run_navigator()


@signals.registered_handler("paint/erase")
def erase(easel):
    """
    Erase one step backward
    """
    easel.erase()


def _convert_color(color):
    clutter_color = Clutter.Color.alloc()
    clutter_color.from_string(color)
    rgba = ()
    string = clutter_color.to_string()
    for idx in range(1, 9, 2):
        rgba += (int(string[idx:idx+2], 16),)
    return rgba
