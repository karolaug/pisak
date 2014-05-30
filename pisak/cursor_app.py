import sys

from gi.repository import Clutter, Mx

from pisak import switcher_app

import pisak.speller.widgets  # @UnusedImport
import pisak.layout  # @UnusedImport
import pisak.cursor  # @UnusedImport
import os.path


class PisakSpellerStage(Clutter.Stage):
    SCRIPT_PATH = os.path.join(os.path.split(__file__)[0], "cursor_app.json")

    def __init__(self, context):
        super().__init__()
        self.context = context
        self._load_script()

    def _load_script(self):
        Mx.Button() # workaround for GI loader
        self.script = Clutter.Script()
        self.script.load_from_file(self.SCRIPT_PATH)
        self.view_actor = self.script.get_object("main")
        self.set_layout_manager(Clutter.BoxLayout())
        self.add_child(self.view_actor)


class PisakSpellerApp(switcher_app.Application):
    """
    Pisak speller app with pisak speller stage.
    """
    def create_stage(self, argv):
        stage = PisakSpellerStage(self.context)
        stage.set_fullscreen(True)
        return stage


if __name__ == "__main__":
    PisakSpellerApp(sys.argv).main()
