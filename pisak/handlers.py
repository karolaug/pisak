'''
ClutterScript signal handler library
'''
from pisak import signals


@signals.registered_handler("general/hello_world")
def say_hello(*args):
    """
    Print standard acknowledging message
    """
    print("Hello World!")


@signals.registered_handler("general/exit")
def exit_app(source, *args):
    source.get_stage().destroy()


@signals.registered_handler("general/start_group")
def start_group(source, *args):
    """
    Start scanning group
    """
    if source.get_property("mapped"):
        source.start_cycle()


@signals.registered_handler("scanning/set_pending_group")
def set_pending_group(source, *args):
    source.get_stage().pending_group = source


@signals.registered_handler("general/switch_label")
def switch_label(button):
    button.switch_label()


@signals.registered_handler("general/switch_icon")
def switch_icon(button):
    button.switch_icon()
