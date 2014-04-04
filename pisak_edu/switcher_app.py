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
        self.switcher = Switcher()


class SwitcherInput(GObject.GObject):
    __gsignals__ = {
        "switcher-select": (GObject.SIGNAL_RUN_FIRST, None, ())
    }


class MouseSwitcherInput(SwitcherInput):
    def __init__(self, stage):
        super().__init__()
        self.stage = stage
        self.stage.connect("button-release-event", self._button_handler)

    def _button_handler(self, source, event):
        self.emit("switcher-select")
        
    
class KeyboardSwitcherInput(SwitcherInput):
    SWITCHER_KEY_VALUE = 0x20 # space
    def __init__(self, stage):
        super().__init__()
        self.stage = stage
        self.stage.connect("key-release-event", self._key_handler)
    
    def _key_handler(self, source, event):
        if event.keyval == self.SWITCHER_KEY_VALUE:
            self.emit("switcher-select")


class Switcher(object):
    def __init__(self):
        self.cycle_stack = []
        self.inputs = {}
        self.timeout_tag = None
    
    def push_cycle(self, cycle):
        if self.cycle_stack:
            self.cycle_stack[-1].stop()  
        self.cycle_stack.append(cycle)
        self.cycle_stack[-1].expose_next()
        self.timeout_tag = object()
        Clutter.threads_add_timeout(0, self.cycle_stack[-1].interval, self.switcher_timeout, self.timeout_tag)
    
    def add_input(self, switcher_input):
        handler_id = switcher_input.connect("switcher-select", self._select)
        self.inputs[switcher_input] = handler_id
    
    def remove_input(self, switcher_input):
        handler_id = self.inputs.pop(switcher_input)
        switcher_input.disconnect(handler_id)
        
    def switcher_timeout(self, source):
        if source == self.timeout_tag:
            self.cycle_stack[-1].expose_next()
            return True
        else:
            return False
    
    def _select(self, source):
        selection = self.cycle_stack[-1].select()
        if selection:
            self.push_cycle(selection)
            

