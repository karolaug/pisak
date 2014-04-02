"""
Basic classes for application using switcher
"""
from gi.repository import GObject, Clutter

class Context(object):
    """
    Switcher application context. Provides to application-wide components such as input and switcher timing.
    """
    def __init__(self, application):
        """
        
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
    SWITCHER_KEY_VALUE = 0x20 # space
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
    def add_cycle(context):
        context.switcher.push_cycle(cycle)
    return add_cycle

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
            

