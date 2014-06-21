import sys
import os.path

from gi.repository import Clutter, Mx

from pisak import switcher_app, unit

import pisak.layout  # @UnusedImport

VIEW_PATHS = {
    "game_screen": "brain_flippers/stroop/main_game_screen.json",
    "rules_changed": "brain_flippers/stroop/rules_changed_screen.json"
}
COLORS = [
    "red", "yellow", "green", "blue"
]

class BrainStroopStage(Clutter.Stage):
    INITIAL_VIEW = "rules_changed"
    
    def __init__(self, context):
        super().__init__()
        self.set_layout_manager(Clutter.BinLayout())
        black = Clutter.Color.new(0, 0, 0, 255)
        self.set_background_color(black)
        self._load_script()

    def _load_script(self):
        self.script = Clutter.Script()
        self.script.load_from_file(VIEW_PATHS[self.INITIAL_VIEW])
        view_actor = self.script.get_object("main")
        self.add_child(view_actor)
        

class BrainStroopApp(switcher_app.Application):
    """
    Brain stroop app with brain stroop stage.
    """
    def create_stage(self, argv):
        stage = BrainStroopStage(self.context)
        stage.set_size(unit.size_pix[0], unit.size_pix[1])
        stage.set_fullscreen(True)
        return stage

if __name__ == "__main__":
    BrainStroopApp(sys.argv).main()
