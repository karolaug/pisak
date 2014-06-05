'''
Does button work?
'''
import sys
from pisak import switcher_app
from gi.repository import Clutter, Mx, GObject


def say_hello(*args):
    print("Hello")


def resolve_name(handler_name):
    """
    Resolve python name to python value in current namespace
    """
    name_parts = handler_name.split('.')
    current = sys.modules[__name__]
    for part in name_parts:
        current = current.__dict__[part]
    return current

def resolve_handler(handler_name):
    function = resolve_name(handler_name)
    if callable(function):
        return function
    else:
        raise "Specified handler is not a function"


def python_connect(script, gobject, signal, handler, target, flags):
    function = resolve_handler(handler)
    gobject.connect_object(signal, function, target, flags)


class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        Mx.Style.get_default()
        script = Clutter.Script()
        script.load_from_file("signals.json")
        script.connect_signals_full(python_connect)
        main_actor = script.get_object("main")
        self.add_child(main_actor)
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return ButtonStage()
        

if __name__ == '__main__':
    ButtonApp(sys.argv).main()