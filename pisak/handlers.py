'''
ClutterScript signal handler library
'''
from pisak import signals
from gi.repository import Clutter

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


@signals.registered_handler("general/kill_group")
def kill_group(source, *args):
    """
    Stop scanning group
    """
    source.killed = True


@signals.registered_handler("scanning/toggle_pause_group")
def toggle_pause_group(source, *args):
    """
    Pause or restart to scan group
    """
    source.paused = not source.paused


@signals.registered_handler("pager/scan_page")
def scan_page(pager):
    pager.scan_page()


@signals.registered_handler("pager/next_page")
def next_page(pager):
    pager.next_page()


@signals.registered_handler("pager/toggle_automatic")
def toggle_automatic(pager):
    if not pager.is_running:
        pager.run_automatic()
    else:
        pager.stop_automatic()


@signals.registered_handler("scanning/set_pending_group")
def set_pending_group(source, *args):
    source.strategy.group.parent_group = source.strategy.unwind_to
    source.get_stage().pending_group = source


@signals.registered_handler("general/switch_label")
def switch_label(button):
    button.switch_label()


@signals.registered_handler("general/switch_icon")
def switch_icon(button):
    button.switch_icon()
