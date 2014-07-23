"""
Basic classes for application using switcher
"""
from gi.repository import GObject, Clutter, Mx
from pisak import res


class Application(object):
    """
    Abstract application class. This is the entry point for switcher apps.
    """

    """
    Path to default CSS style
    """
    CSS_RES_PATH = "style.css"

    def __init__(self, argv):
        """
        Initialize the aplication.
        :param: argv application arguments
        """
        self._initialize_context()
        self._initialize_stage(argv)

    def _initialize_style(self):
        # load default style
        self.style = Mx.Style.get_default()
        style_path = res.get(self.CSS_RES_PATH)
        try:
            self.style.load_from_file(style_path)
        except GObject.GError:
            raise Exception("Failed to load default style")

    def _initialize_stage(self, argv):
        # create and set up a Clutter.Stage
        Clutter.init(argv)
        self._initialize_style()
        self.stage = self.create_stage(argv)
        self.stage.connect("destroy", lambda _: Clutter.main_quit())

    def create_stage(self, argv):
        """
        Abstract method which should create Clutter.Stage instance
        :param: argv application arguments
        """
        raise NotImplementedError()

    def _initialize_context(self):
        self.context = Context(self)

    def push_view(self, view_actor):
        '''
        Show new view on top.
        @param view_actor New view
        '''
        self.stage.push_view(view_actor)

    def pop_view(self):
        '''
        Discard current view and go back to previous
        '''
        self.stage.pop_view()

    def main(self):
        """
        Starts the application main loop.
        """
        self.stage.show_all()
        Clutter.main()


class Context(object):
    """
    Switcher application context. Provides to application-wide components such as input and switcher timing.
    """
    def __init__(self, application):
        """
        Create context for an application.
        """
        self.application = application
        self._initialize_switcher()

    def _initialize_switcher(self):
        self.switcher = Switcher(self)


class SwitcherInput(GObject.GObject):
    __gsignals__ = {
        "switcher-select": (GObject.SIGNAL_RUN_FIRST, None, ())
    }


class KeyboardSwitcherInput(SwitcherInput):
    SWITCHER_KEY_VALUE = 0x20  # space

    def __init__(self, stage):
        super().__init__()
        self.stage = stage
        self.stage.connect("key-release-event", self._key_handler)

    def _key_handler(self, source, event):
        if event.keyval == self.SWITCHER_KEY_VALUE:
            self.emit("switcher-select")


class Cycle(object):
    """
    Abstract base class for switcher cycles.
    """
    def expose_next(self):
        """
        Highlight next cycle element.
        """
        raise NotImplementedError

    def has_next(self):
        """
        Test whether there are any more elements to expose.
        """
        raise NotImplementedError

    def stop(self):
        """
        Stop the cycle, clean up.
        """
        raise NotImplementedError

    def select(self):
        """
        Select current element.
        @return: Function which handles and applies the selection.
        """
        raise NotImplementedError


def selection_add_cycle(cycle):
    """
    Closure constructor for adding a new cycle
    """
    def add_cycle(context):
        context.switcher.push_cycle(cycle)
    return add_cycle


def selection_activate_actor(actor):
    """
    Closure constructor for activating and element
    """
    def activate_actor(context):
        actor.emit("activate")
    return activate_actor


class Switcher(object):
    def __init__(self, context):
        self.context = context
        self.cycle_stack = []
        self.inputs = {}
        self.timeout_token = None

    def push_cycle(self, cycle):
        if self.cycle_stack:
            self.cycle_stack[-1].stop()
        self.cycle_stack.append(cycle)
        self._start_cycle()

    def add_input(self, switcher_input):
        handler_id = switcher_input.connect("switcher-select", self._select)
        self.inputs[switcher_input] = handler_id

    def remove_input(self, switcher_input):
        handler_id = self.inputs.pop(switcher_input)
        switcher_input.disconnect(handler_id)

    def _start_cycle(self):
        # show first element immediately on start
        self._expose_next()
        self.timeout_token = object()
        Clutter.threads_add_timeout(0, self.cycle_stack[-1].interval, self.switcher_timeout, self.timeout_token)

    def _expose_next(self):
        self.cycle_stack[-1].expose_next()

    def _has_next(self):
        return self.cycle_stack[-1].has_next()

    def _stop_cycle(self):
        self.cycle_stack[-1].stop()
        self.cycle_stack.pop()
        if self.cycle_stack:
            self._start_cycle()

    def switcher_timeout(self, token):
        if self.timeout_token != token:
            # timeout event not from current cycle
            return False
        elif self._has_next():
            self._expose_next()
            return True
        else:
            self._stop_cycle()
            return False

    def _select(self, source):
        selection = self.cycle_stack[-1].select()
        selection(self.context)
