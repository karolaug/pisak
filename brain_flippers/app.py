import sys

from gi.repository import Clutter, Mx

from pisak import switcher_app

import pisak.widgets  # @UnusedImport
import pisak.layout  # @UnusedImport


class BrainFlipperStage(Clutter.Stage):
    SCRIPT_PATH = "brain_flippers/results_screen.json"

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


class BrainFlipperApp(switcher_app.Application):
    """
    Brain flipper app with brain flipper stage.
    """
    def create_stage(self, argv):
        stage = BrainFlipperStage(self.context)
        stage.set_fullscreen(True)
        return stage


if __name__ == "__main__":
    BrainFlipperApp(sys.argv).main()
