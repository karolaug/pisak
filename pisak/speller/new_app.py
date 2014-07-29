import sys
import os.path

from gi.repository import Clutter, Mx

from pisak import switcher_app, signals

import pisak.layout  # @UnusedImport
import pisak.scanning  # @UnusedImport

import pisak.handlers  # @UnusedImport
import pisak.speller.handlers  # @UnusedImport


_PATH = os.path.abspath(os.path.split(__file__)[0])


def _local_get(relative):
    return os.path.join(_PATH, relative)


SCRIPT_PATHS = {
    "row": _local_get("speller_row.json"),
    "column": _local_get("speller_column.json"),
    "combined": _local_get("speller_combined.json")
}


class PisakSpellerStage(Clutter.Stage):
    STYLESHEET_PATH = _local_get("speller_stylesheet.css")

    def __init__(self, context, script_path):
        super().__init__()
        self.context = context
        self.script_path = script_path
        self._load_script()
        self._load_stylesheet()

    def _load_script(self):
        self.script = Clutter.Script()
        self.script.load_from_file(self.script_path)
        self.script.connect_signals_full(signals.connect_registered)
        self.view_actor = self.script.get_object("main")
        self.set_layout_manager(Clutter.BinLayout())
        self.add_child(self.view_actor)

    def _load_stylesheet(self):
        Mx.Style.get_default().load_from_file(self.STYLESHEET_PATH)


class PisakSpellerApp(switcher_app.Application):
    """
    Pisak speller app with pisak speller stage.
    """
    def create_stage(self, argv):
        script_path = SCRIPT_PATHS[argv[1]]
        stage = PisakSpellerStage(self.context, script_path)
        stage.set_size(1366, 768)
        stage.set_fullscreen(True)
        return stage


def usage():
    print("Usage: new_app.py VARIANT")
    print(
        "Where variant is on of:\n"
        "  row - speller with row layout\n"
        "  column - speller with column layout\n"
        "  combined - speller with combined layout")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    elif sys.argv[1] not in SCRIPT_PATHS:
        usage()
    else:
        PisakSpellerApp(sys.argv).main()
