'''
Classes for defining scanning in JSON layouts
'''
from gi.repository import Clutter, GObject, Mx, Gdk

from pisak import properties

from concept import audio
import logging


_LOG = logging.getLogger(__name__)

class Scannable(object):
    """
    Interface of object scannable by switcher groups. Switcher groups expect
    widgets implement this interface.
    """
    def activate(self):
        """
        Performs widgets action.
        """
        raise NotImplementedError()

    def enable_hilite(self):
        """
        Enables hilite style for this widget.
        """
        raise NotImplementedError()

    def disable_hilite(self):
        """
        Disables hilite style for this widget.
        """
        raise NotImplementedError()

    def enable_scanned(self):
        """
        Enables scanned style for this widget.
        """
        raise NotImplementedError()

    def disable_scanned(self):
        """
        Enables hilite style for this widget.
        """
        raise NotImplementedError()


class StylableScannable(object):
    """
    Partial implementation of Scannable interface for stylable widgets.
    Hilighted and scanned widgets are marked with CSS pseudoclasses.
    """
    def enable_hilite(self):
        self.style_pseudo_class_add("hover")

    def disable_hilite(self):
        self.style_pseudo_class_remove("hover")

    def enable_scanned(self):
        self.style_pseudo_class_add("scanning")

    def disable_scanned(self):
        self.style_pseudo_class_remove("scanning")


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
        if isinstance(element, Group):
            if not self.group.paused:
                self.group.stop_cycle()
                if not self.group.killed:
                    element.parent_group = self.group
                    element.start_cycle()
        elif hasattr(element, "activate"):
            # set potential next group
            self.group.stage.pending_group = self.unwind_to
            if not self.group.killed:
                element.activate()
            if not self.group.paused:
                self.group.stop_cycle()
            if not self.group.killed and not self.group.paused:
                # launch next group
                if self.group.stage.pending_group:
                    self.group.stage.pending_group.start_cycle()
                else:
                    if self.group.get_stage():
                        self.group.start_cycle()
        else:
            raise Exception("Unsupported selection")

    def unwind(self):
        if self.unwind_to is not None:
            self.group.stop_cycle()
            self.unwind_to.start_cycle()
        else:
            self.group.stop_cycle()
            self.group.parent_group.start_cycle()

    def get_current_element(self):
        """
        Abstract method to extract currently highlighted element from an
        internal strategy state.

        :returns: currently highlighed element
        """
        raise NotImplementedError("Incomplete strategy implementation")


class ScanningException(Exception):
    pass


class Group(Clutter.Actor, properties.PropertyAdapter):
    """
    Container for grouping widgets for scanning purposes.
    """
    __gtype_name__ = "PisakScanningGroup"

    __gproperties__ = {
        "strategy": (
            Strategy.__gtype__,
            "", "",
            GObject.PARAM_READWRITE),
        "scanning-hilite": (
            GObject.TYPE_BOOLEAN,
            "", "", False,
            GObject.PARAM_READWRITE),
        "selector": (
            GObject.TYPE_STRING, "", "",
            "mouse", GObject.PARAM_READWRITE)
    }

    def __init__(self):
        self._strategy = None
        self.paused = False
        self.killed = False
        self._scanning_hilite = False
        super().__init__()
        self.set_layout_manager(Clutter.BinLayout())
        # handle only when active
        # self.connect("key-release-event", self.key_release)

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

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, value):
        self._selector = value

    @property
    def scanning_hilite(self):
        return self._scanning_hilite

    @scanning_hilite.setter
    def scanning_hilite(self, value):
        self._scanning_hilite = value
        if not value:
            self.disable_scan_hilite("scanning")

    def get_subgroups(self, flag=None):
        '''
        Generator of all subgroups of the group.
        '''
        to_scan = self.get_children()
        while len(to_scan) > 0:
            current = to_scan.pop()
            if flag == "all":
                if isinstance(current, Group) \
                        or isinstance(current, Scannable) \
                        or isinstance(current, Mx.Button):
                    yield current
            else:
                if isinstance(current, Group) \
                        or isinstance(current, Scannable) \
                        or (isinstance(current, Mx.Button)
                        and not current.get_disabled()):
                    yield current
            if not isinstance(current, Group):
                to_scan.extend(current.get_children())

    def start_cycle(self):
        _LOG.debug("Starting group {}".format(self.get_id()))
        self.stage = self.get_stage()
        if self.stage is None:
            message = \
                "Started cycle in unmapped group: {}".format(self.get_id())
            raise ScanningException(message)
        if self.selector == 'mouse':
            self._handler_token = self.stage.connect("button-release-event",
                                                     self.button_release)
        elif self.selector == 'keyboard':
            self._handler_token = self.connect("key-release-event",
                                               self.key_release)
        elif self.selector == 'mouse-switch':
            self._handler_token = self.stage.connect("button-release-event",
                                                     self.button_release)
            display = Gdk.Display.get_default()
            screen = display.get_default_screen()
            display.warp_pointer(screen, 0, 0)
            self.stage.hide_cursor()

        else:
            _LOG.warning("Unknown selector: ", self.selector)
            return None
        self.get_stage().set_key_focus(self)
        if self.scanning_hilite:
            self.enable_scan_hilite()
        self.strategy.start()

    def stop_cycle(self):
        action = {'mouse': self.stage.disconnect,
                  'mouse-switch': self.stage.disconnect,
                  'keyboard': self.disconnect}
        self.stage.set_key_focus(None)
        try:
            action[self.selector](self._handler_token)
        except AttributeError:
            print('No such selector:', self.selector)
        if self.scanning_hilite:
            self.disable_scan_hilite()
        self.strategy.stop()

    @staticmethod
    def key_release(source, event):
        if event.unicode_value == ' ':
            source.strategy.select()
        return True

    def button_release(self, source, event):
        self.strategy.select()
        return False

    def recursive_apply(self, test, operation, flag=None):
        if flag == "all":
            subgroups = self.get_subgroups("all")
        else:
            subgroups = self.get_subgroups()
        for s in subgroups:
            if test(s):
                operation(s)
            elif isinstance(s, Group):
                s.recursive_apply(test, operation, flag)

    def enable_hilite(self):
        self.recursive_apply(
            lambda s: hasattr(s, "enable_hilite"),
            lambda s: s.enable_hilite())

    def disable_hilite(self):
        self.recursive_apply(
            lambda s: hasattr(s, "disable_hilite"),
            lambda s: s.disable_hilite(), "all")    

    def enable_scan_hilite(self):
        self.recursive_apply(
            lambda s: hasattr(s, "enable_scanned"),
            lambda s: s.enable_scanned())

    def disable_scan_hilite(self):
        self.recursive_apply(
            lambda s: hasattr(s, "disable_scanned"),
            lambda s: s.disable_scanned(), "all")


class RowStrategy(Strategy, properties.PropertyAdapter):
    __gtype_name__ = "PisakRowStrategy"

    __gproperties__ = {
        "interval": (
            GObject.TYPE_UINT,
            "", "",
            0, GObject.G_MAXUINT, 1000,
            GObject.PARAM_READWRITE),
        "max-cycle-count": (
            GObject.TYPE_INT,
            "", "",
            -1, GObject.G_MAXINT, 2,
            GObject.PARAM_READWRITE),
        "unwind-to": (
            Group.__gtype__,
            "", "",
            GObject.PARAM_READWRITE),
        "scanning-audio-path": (
            GObject.TYPE_STRING, "", "",
            "None", GObject.PARAM_READWRITE),
        "selection-audio-path": (
            GObject.TYPE_STRING, "", "",
            "None", GObject.PARAM_READWRITE)
    }

    def __init__(self):
        self._group = None
        self._allocation_slot = None
        self._subgroups = []
        self.index = None
        super().__init__()
        self.interval = 1000
        self._max_cycle_count = 2
        self._buttons = []
        self._unwind_to = None
        self.timeout_token = None
        self._scanning_audio_path = "None"
        self._selection_audio_path = "None"

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = int(value)

    @property
    def max_cycle_count(self):
        return self._max_cycle_count

    @max_cycle_count.setter
    def max_cycle_count(self, value):
        self._max_cycle_count = int(value)

    @property
    def unwind_to(self):
        return self._unwind_to

    @unwind_to.setter
    def unwind_to(self, value):
        self._unwind_to = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        if self.group is not None:
            message = "Group strategy reuse, old {}, new {}"
            _LOG.warning(message.format(self.group.get_id(), value.get_id()))
            _LOG.debug("new {}, old {}".format(self.group, value))
            self.group.disconnect(self._allocation_slot)
        self._group = value
        if self.group is not None:
            self._allocation_slot = \
                self.group.connect("allocation-changed", self.update_rows)

    @property    
    def scanning_audio_path(self):
        return self._scanning_audio_path

    @scanning_audio_path.setter
    def scanning_audio_path(self, value):
        self._scanning_audio_path = value                

    @property    
    def selection_audio_path(self):
        return self._selection_audio_path

    @selection_audio_path.setter
    def selection_audio_path(self, value):
        self._selection_audio_path = value                


    def update_rows(self, *args):
        _LOG.debug("Row layout allocation changed")
        if self.index is not None:
            selection = self._subgroups[self.index]
            if hasattr(selection, "disable_hilite"):
                selection.disable_hilite()
        self.compute_sequence()
        self.index = None

    def compute_sequence(self):
        subgroups = list(self.group.get_subgroups())
        key_function = lambda a: list(reversed(a.get_transformed_position()))
        subgroups.sort(key=key_function)
        self._subgroups = subgroups

    def start(self):
        self.compute_sequence()
        if len(self._subgroups) == 0:
            # stop immediately
            self.index = None
            Clutter.threads_add_timeout(0, self.interval, self.cycle_timeout, self.timeout_token)
        else:
            self.index = None
            self._cycle_count = 0
            self._expose_next()
            self.timeout_token = object()
            Clutter.threads_add_timeout(0, self.interval, self.cycle_timeout, self.timeout_token)

    def stop(self):
        self.timeout_token = None
        self._stop_cycle()

    def _stop_cycle(self):
        if self.index is not None:
            selection = self._subgroups[self.index]
            if hasattr(selection, "disable_hilite"):
                selection.disable_hilite()
            elif isinstance(selection, Group):
                selection.disable_hilite()

    def _expose_next(self):
        if self.scanning_audio_path != "None":
            self.play_audio(self.scanning_audio_path)
        if self.index is not None:
            selection = self._subgroups[self.index]
            if hasattr(selection, "disable_hilite"):
                selection.disable_hilite()
            elif isinstance(selection, Group):
                selection.disable_hilite()
            self.index = (self.index + 1) % len(self._subgroups)
        else:
            self.index = 0
        selection = self._subgroups[self.index]
        if hasattr(selection, "enable_hilite"):
            selection.enable_hilite()
        elif isinstance(selection, Group):
            selection.enable_hilite()
        if self.index == len(self._subgroups) - 1:
            self._cycle_count += 1

    def _has_next(self):
        if len(self._subgroups) == 0:
            return False
        else:
            return (self.max_cycle_count == -1) or \
                (self._cycle_count < self.max_cycle_count)

    def cycle_timeout(self, token):
        if self.timeout_token != token:
            # timeout event not from current cycle
            return False
        elif self._has_next():
            if not self.group.paused:
                self._expose_next()
            return True
        else:
            self.unwind()
            return False

    def get_current_element(self):
        if self.selection_audio_path != "None":
            self.play_audio(self.selection_audio_path)
        return self._subgroups[self.index]

    def play_audio(self, audio_path):
        audiofile = audio.AudioFile('pisak/res/sounds/' + audio_path)    
        audiofile.play()
        audiofile.close()
