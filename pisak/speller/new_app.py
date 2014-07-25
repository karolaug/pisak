import sys

from gi.repository import Clutter, Mx

from pisak import switcher_app, signals
from pisak.speller import widgets

import pisak.layout  # @UnusedImport
import pisak.scanning  # @UnusedImport

import pisak.handlers  # @UnusedImport
import pisak.speller.handlers  # @UnusedImport


class PisakSpellerStage(Clutter.Stage):
    STYLESHEET_PATH = "speller_stylesheet.css"
    
    def __init__(self, context):
        super().__init__()
        self.context = context
        self._load_script()
        #self._load_stylesheet()

    def _load_script(self):
        self.script = Clutter.Script()
        self.script.load_from_file(SCRIPT_PATH)
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
        stage = PisakSpellerStage(self.context)
        stage.set_size(1366, 768)
        stage.set_fullscreen(True)
        return stage
    

if __name__ == "__main__":
    def usage():
        print("Parameters:\n"
              " row - speller with row layout\n"
              " column - speller with column layout\n"
              " combined - speller with combined layout"
              )
    try:
        SCRIPT_PATH = {
            "row": "pisak/speller/speller_row.json",
            "column": "pisak/speller/speller_column.json",
            "combined": "pisak/speller/speller_combined.json"
            }[sys.argv[1]]
        PisakSpellerApp(sys.argv).main()
    except IndexError:
        print("No parameters passed.")
        usage()
