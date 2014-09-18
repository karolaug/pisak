"""
Module with widgets specific to pisak main panel
"""
import os.path

from gi.repository import Mx

from pisak import widgets, res


LOGO_PATH = os.path.join(res.PATH, "logo_pisak.png")


class Button(widgets.Button):
    """
    Main panel button that can be styled by CSS.
    """
    __gtype_name__ = "PisakMainPanelButton"


class PisakLogo(Mx.Image):
    """
    Widget displaying PISAK project logo.
    """
    __gtype_name__ = "PisakLogo"
    
    def __init__(self):
        super().__init__()
        self.set_from_file(LOGO_PATH)
