from pisak import switcher_app
from gi.repository import Clutter, Mx
import sys
import pisak.speller.widgets


class PisakSpellerStage(Clutter.Stage):
    SCRIPT_PATH = 'speller_column.json'
    def __init__(self, context):
        super().__init__()
        self.context = context
        self._load_script()

    def _load_script(self):
        self.script = Clutter.Script()
        self.script.load_from_file(self.SCRIPT_PATH)
        view_actor = self.script.get_object("speller_view")
        self.set_layout_manager(Clutter.BinLayout())
        self.add_child(view_actor)


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
