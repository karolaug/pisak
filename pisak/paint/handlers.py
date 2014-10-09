'''
ClutterScript paint specific signal handler library
'''
from gi.repository import Clutter

from pisak import signals
from pisak.paint import widgets


@signals.registered_handler("paint/set_line_color")
def set_line_color(button):
    """
    Set easel line color
    """
    easel = button.target
    easel.line_rgba = widgets.convert_color(button.get_background_color())


@signals.registered_handler("paint/set_line_width")
def set_line_width(button):
    """
    Set easel line width
    """
    easel = button.target
    easel.line_width = int(button.get_label().split(" ")[0])


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
