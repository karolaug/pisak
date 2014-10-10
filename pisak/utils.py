"""
Module with various Pisak utility functions.
"""
from gi.repository import Clutter


def convert_color(color):
    """
    Return tuple with color bands normalized int values converted from
    the given color.
    :param color: instance of ClutterColor or string color description
    in one of the formats accepted by ClutterColor
    """
    if isinstance(color, Clutter.Color):
        clutter_color = color
    else:
        clutter_color = Clutter.Color.new(0, 0, 0, 255)
        clutter_color.from_string(color)
    return hex_to_rgba(clutter_color.to_string())


def hex_to_rgba(value):
    """
    Convert given color description in a hexadecimal format
    to normalized int values for separate color bands.
    :param value: color desc in hexadecimal format as returned by ClutterColor
    to_string method, that is: #rrggbbaa
    """
    rgba = ()
    for idx in range(1, 9, 2):
        rgba += (int(value[idx:idx+2], 16)/255.,)
    return rgba
    
