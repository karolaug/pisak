import sys

from gi.repository import Clutter, Mx

from pisak import switcher_app
from brain_flippers import score_manager

import pisak.widgets  # @UnusedImport
import pisak.layout  # @UnusedImport
import os.path

VIEW_PATHS = {
  "high_scores": "best_result_screen.json",
  "enter_score": "user_result_screen.json",
  "main_menu": None,
  "game_screen": None
}


class BrainFlipperStage(Clutter.Stage):
    INITIAL_VIEW = "enter_score"

    def __init__(self, context):
        super().__init__()
        self._init_views()
        self.context = context
        self._load_script()

    def _init_views(self):
        current_path = os.path.split(__file__)[0]
        self.views = {}
        for name, path in VIEW_PATHS.items():
            if path is None:
                continue
            view_script = Clutter.Script()
            view_script.load_from_file(os.path.join(current_path, path))
            self.views[name] = view_script

    def _load_script(self):
        self.script = self.views[self.INITIAL_VIEW]
        self.view_actor = self.script.get_object("main")
        self.set_layout_manager(Clutter.BinLayout())
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
