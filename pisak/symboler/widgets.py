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


class ProgressBar(widgets.ProgressBar):
    """
    Widget indicating progress, with label on top, can by styled by CSS.
    """
    __gtype_name__ = "PisakSymbolerProgressBar"
    
    def __init__(self):
        super().__init__()
        self.label = Mx.Label()
        self.label.set_style_class("PisakSymbolerProgressBar")
        self.bar.get_children()[0].set_style_class("PisakSymbolerProgressBar")
        self.bar.set_style_class("PisakSymbolerProgressBar")


class TilesSource(pager.DataSource):
    """
    Data source generating tiles with symbols.
    """
    __gtype_name = "PisakSymbolerTilesSource"
