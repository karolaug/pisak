'''
Basic implementation of sliding page widget.
'''
from gi.repository import Clutter, GObject
from pisak import properties


class DataSource(GObject.GObject):
    pass


class PagerWidget(Clutter.Actor, properties.PropertyAdapter):
    __gtype_name__ = "PisakPagerWidget"

    __gproperties__ = {
        "data-source": (DataSource.__gtype__, "", "", GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        pass
