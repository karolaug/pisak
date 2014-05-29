'''
Classes for defining scanning in JSON layouts
'''
from gi.repository import Clutter, GObject

class Strategy(GObject.GObject):
    """
    Abstract base class for scanning strategies.
    """
    pass


class Group(Clutter.Actor):
    """
    Container for grouping widgets for scanning purposes.
    """
    __gtype_name__ = "PisakScanningGroup"
    
    __gproperties = {
        "strategy": (
            Strategy.__gtype__,
            "", "",
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        self.strategy = None

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        self._strategy = value


class RowStrategy(Strategy):
    __gtype_name__ = "PisakRowStrategy"
    
    __gproperties = {
        "interval": (
            GObject.TYPE_INT,
            "", "",
            0, GObject.G_MAXUINT, 1000,
            GObject.PARAM_READWRITE)
    }
    
    def __init__(self):
        super().__init__()
        self.interval = 1000
    
    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = int(value)
