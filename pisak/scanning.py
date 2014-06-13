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
        """
        Reference to a group which owns the strategy.
        """
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    def select(self):
        """
        Selects currently highlighted element.
        """
        element = self.get_current_element()
        element.emit("clicked")

    def get_current_element(self):
        """
        Abstract method to extract currently highlighted element from an
        internal strategy state.

        :returns: currently highlighed element
        """
        raise NotImplementedError("Incomplete strategy implementation")


class Group(Clutter.Actor):
    """
    Container for grouping widgets for scanning purposes.
    """
    __gtype_name__ = "PisakScanningGroup"
    
    __gproperties__ = {
        "strategy": (
            Strategy.__gtype__,
            "", "",
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        self._strategy = None
        super().__init__()
        self.set_layout_manager(Clutter.BinLayout())
        self.connect("key-release-event", self.key_release)

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

    def do_set_property(self, spec, value):
        """
        Introspect object properties and set the value.
        """
        attribute = self.__class__.__dict__.get(spec.name)
        if attribute is not None and isinstance(attribute, property):
            attribute.fset(self, value)
        else:
            raise ValueError("No such property", spec.name)

    def do_get_property(self, spec):
        """
        Introspect object properties and get the value.
        """
        attribute = self.__class__.__dict__.get(spec.name)
        if attribute is not None and isinstance(attribute, property):
            return attribute.fget(self)
        else:
            raise ValueError("No such property", spec.name)

    def get_subgroups(self):
        '''
        Generator of all subgroups of the group.
        '''
        to_scan = self.get_children()
        while len(to_scan) > 0:
            current = to_scan.pop()
            if isinstance(current, Group) or isinstance(current, Mx.Button):
                yield current
            if not isinstance(current, Group):
                to_scan.extend(current.get_children())
    
    def start_cycle(self):
        stage = self.get_stage()
        stage.set_key_focus(self)
        self.strategy.start()

    @staticmethod
    def key_release(source, event):
        if event.unicode_value == ' ':
            source.strategy.select()

    def enable_hilite(self):
        #for s in self.get_subgroups():
        #    if isinstance(s, Mx.Stylable):
        #        s.set_style_pseudo_class("hover")
        #    elif isinstance(s, Group):
        #        s.enable_hilite()
        self.set_background_color(Clutter.Color.new(128, 128, 128, 255))

    def disable_hilite(self):
        #for s in self.get_subgroups():
        #    if isinstance(s, Mx.Stylable):
        #        s.set_style_pseudo_class("hover")
        #    elif isinstance(s, Group):
        #        s.enable_hilite()
        self.set_background_color(Clutter.Color.new(0, 0, 0, 0))


class RowStrategy(Strategy):
    __gtype_name__ = "PisakRowStrategy"

    __gproperties__ = {
        "interval": (
            GObject.TYPE_UINT,
            "", "",
            0, GObject.G_MAXUINT, 1000,
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        self._group = None
        super().__init__()
        self.interval = 1000
        self._buttons = []
        self.timeout_token = None

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = int(value)

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        if self.group is not None:
            self.group.disconnect("allocation-changed")
        self._group = value
        if self.group is not None:
            self.group.connect("allocation-changed", self.update_rows)

    def update_rows(self, *args):
        selection = self._subgroups[self.index]
        if isinstance(selection, Mx.Stylable):
            selection.set_style_pseudo_class("")
        self.compute_sequence()

    def do_set_property(self, spec, value):
        """
        Introspect object properties and set the value.
        """
        attribute = self.__class__.__dict__.get(spec.name)
        if attribute is not None and isinstance(attribute, property):
            attribute.fset(self, value)
        else:
            raise ValueError("No such property", spec.name)

    def do_get_property(self, spec):
        """
        Introspect object properties and get the value.
        """
        attribute = self.__class__.__dict__.get(spec.name)
        if attribute is not None and isinstance(attribute, property):
            return attribute.fget(self)
        else:
            raise ValueError("No such property", spec.name)

    def compute_sequence(self):
        subgroups = list(self.group.get_subgroups())
        key_function = lambda a: a.get_transformed_position()[1]
        subgroups.sort(key=key_function)
        self._subgroups = subgroups

    def start(self):
        self.compute_sequence()
        self.index = None
        self._expose_next()
        self.timeout_token = object()
        Clutter.threads_add_timeout(0, self.interval, self.cycle_timeout, self.timeout_token)

    def _expose_next(self):
        if self.index is not None:
            selection = self._subgroups[self.index]
            if isinstance(selection, Mx.Stylable):
                selection.set_style_pseudo_class("")
            elif isinstance(selection, Group):
                selection.disable_hilite()
            self.index = (self.index + 1) % len(self._subgroups)
        else:
            self.index = 0
        selection = self._subgroups[self.index]
        print(selection.get_id())
        print(selection.get_transformed_position(), selection.get_size())
        if isinstance(selection, Mx.Stylable):
            selection.set_style_pseudo_class("hover")
        elif isinstance(selection, Group):
            selection.enable_hilite()

    def _has_next(self):
        return True

    def cycle_timeout(self, token):
        if self.timeout_token != token:
            # timeout event not from current cycle
            return False
        elif self._has_next():
            self._expose_next()
            return True
        else:
            self._stop_cycle()
            return False

    def get_current_element(self):
        return self._subgroups[self.index]
