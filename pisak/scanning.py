'''
Classes for defining scanning in JSON layouts
'''
from gi.repository import Clutter, GObject, Mx


class Strategy(GObject.GObject):
    """
    Abstract base class for scanning strategies.
    """
    def __init__(self):
        super().__init__()
        self.group = None

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value 


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
        super().__init__()
        self.strategy = None

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        if self.strategy is not None:
            self.strategy.group = None
        self._strategy = value
        if self.strategy is not None:
            self.strategy.group = self
    
    def get_subgroups(self):
        '''
        Generator of all subgroups of the group.
        '''
        to_scan = self.get_children()
        while len(to_scan) > 0:
            current = to_scan.pop()
            yield current
            if not isinstance(current, Group):
                to_scan.extend(current.get_children())
    
    def start_cycle(self, *args):
        print("START CYCLE")


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
        self._buttons = []

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = int(value)

    def compute_sequence(self):
        subgroups = list(self.group.get_subgroups())
        subgroups.sort(key=Clutter.Actor.get_y)
        self._subgroups = subgroups
