import os

from pisak import res
from pisak.symboler import database_manager


SYMBOLS_DIR = res.get("symbols")


def load_all_linear():
    symbols = []
    for current, _subdirs, files in os.walk(SYMBOLS_DIR):
        for symbol_path in [os.path.join(current, name) for name in files]:
            symbols.append(symbol_path)
    database_manager.insert_many_symbols(symbols)
