import sys
import os.path

from gi.repository import Clutter, Mx

from pisak import switcher_app, signals, res

import pisak.layout  # @UnusedImport
import pisak.scanning  # @UnusedImport

import pisak.handlers  # @UnusedImport
import pisak.speller.handlers  # @UnusedImport

class PisakSpellerStage(Clutter.Stage):
    STYLESHEET_PATH = ("pisak/speller/speller_stylesheet.css")

    def __init__(self, context, script_path):
        super().__init__()
        self.context = context
        self.script_path = script_path
        self._load_script()
        #self._load_stylesheet()

    def _load_script(self):
        self.script = Clutter.Script()
        self.script.load_from_file("button_layout.json")
        self.script.connect_signals_full(signals.connect_registered)
        self.view_actor = self.script.get_object("main")
        self.image = self.script.get_object("image")
        self.image.set_from_file(os.path.join(res.PATH, "jagoda.jpg"))
        self.image.set_scale_mode(2)
        self.set_layout_manager(Clutter.BinLayout())
        self.add_child(self.view_actor)

    def _load_stylesheet(self):
        Mx.Style.get_default().load_from_file(self.STYLESHEET_PATH)

class PisakSpellerApp(switcher_app.Application):
    """
    Pisak speller app with pisak speller stage.
    """
    def create_stage(self, argv):
        stage = PisakSpellerStage(self.context, "stage")
        stage.set_size(1366, 768)
        stage.set_fullscreen(True)
        return stage

if __name__ == "__main__":
    PisakSpellerApp(sys.argv).main()
