import os

from pisak import res
from pisak.viewer import database_manager


SYMBOLS_DIR = res.get("symbols")


def load_all_linear():
    for current, _subdirs, files in os.walk(SYMBOLS_DIR):
        for symbol_path in [os.path.join(current, name) for name in files]:
            database_manager.insert_symbol(symbol_path)
