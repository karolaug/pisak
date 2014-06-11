'''
ClutterScript signal handler library
'''

def say_hello(*args):
    """
    Print standard acknowledging message
    """
    print("Hello World!")


def start_group(source, *args):
    """
    Start scanning group
    """
    source.start_cycle()


def exit_app(source, *args):
    source.get_stage().destroy()
