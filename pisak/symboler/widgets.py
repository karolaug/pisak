"""
Module with widgets specific to symboler application.
"""
from gi.repository import Mx

from pisak import widgets, pager


class Button(widgets.Button):
    """
    Button widget, can be styled by CSS.
    """
    __gtype_name__ = "PisakSymbolerButton"


class Slider(widgets.Slider):
    """
    Widget indicating a range of content being displayed, can by styled by CSS.
    """
    __gtype_name__ = "PisakSymbolerSlider"


class TilesSource(pager.DataSource):
    """
    Data source generating tiles with symbols.
    """
    __gtype_name = "PisakSymbolerTilesSource"
