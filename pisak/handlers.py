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

@signals.registered_handler("general/start_group")
def start_group(source, *args):
    """
    Start scanning group
    """
    if source.get_property("mapped"):
        source.start_cycle()

@signals.registered_handler("general/exit")
def exit_app(source, *args):
    source.get_stage().destroy()
