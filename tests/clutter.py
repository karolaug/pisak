"""
Module contains helpers for creating Clutter-based unit tests
"""
import functools
from gi.repository import Clutter

def on_stage(function):
    """
    Decorator which supplies a Clutter stage to a wrapped function.
    """
    @functools.wraps(function)
    def ret(*args):
        stage = Clutter.Stage()
        args = args + (stage,)
        function(*args)
        stage.destroy()
    return ret

