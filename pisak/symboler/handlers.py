import subprocess

from pisak import signals


@signals.registered_handler("symboler/text_to_speech")
def text_to_speech(entry):
    """
    Read the text loud.
    :param entry: symbols entry
    """
    text = entry.get_text()
    if text:
        subprocess.call(["milena_say", text])


@signals.registered_handler("symboler/backspace")
def backspace(entry):
    """
    Delete the last symbol from the entry.
    :param entry: symbols entry
    """
    entry.delete_symbol()


@signals.registered_handler("symboler/clear_all")
def clear_all(entry):
    """
    Clear the whole entry.
    :param entry: symbols entry
    """
    text = entry.clear_all()
