'''
Implementation of signal connecting strategy for ClutterScript. 
'''
import sys

import pisak.handlers  # @UnusedImport


"""
Object or module relative to which signal handlers are named
"""
BASE_NAMESPACE = sys.modules[__name__] 


def resolve_name(handler_name):
    """
    Resolve python name to python value in current namespace
    """
    name_parts = handler_name.split('.')
    current = BASE_NAMESPACE
    for part in name_parts:
        current = current.__dict__[part]
    return current


def resolve_handler(handler_name):
    """
    Resolve handler name and check for callability
    """
    function = resolve_name(handler_name)
    if callable(function):
        return function
    else:
        raise "Specified handler is not a function"


def python_connect(script, gobject, signal, handler, target, flags):
    """
    Implementation of signal connector used by
    ClutterScript.connect_signals_full
    """
    function = resolve_handler(handler)
    gobject.connect_object(signal, function, target, flags)
