from pisak import switcher_app
from gi.repository import Clutter, Mx, Pango
import sys
import pisak.speller.widgets


class PisakSpellerStage(Clutter.Stage):
    SCRIPT_PATH = 'pisak/speller/speller_row.json'
    def __init__(self, context):
        super().__init__()
        self.context = context
        self._load_script()

    def _load_script(self):
        self.script = Clutter.Script()
        self.script.load_from_file(self.SCRIPT_PATH)
        view_actor = self.script.get_object("speller_view")
        for i in view_actor.get_children():
            if type(i) == Mx.Entry: entry = i
        text = entry.get_property("clutter-text")
        text.set_size(94, 200)
        text.set_line_wrap(True)
        text.set_max_length(200)
        self.add_child(view_actor)


class PisakSpellerApp(switcher_app.Application):
    """
    Pisak speller app with pisak speller stage.
    """
    def create_stage(self, argv):
        stage = PisakSpellerStage(self.context)
        stage.set_fullscreen(True)
        return stage


if __name__== "__main__":
    PisakSpellerApp(sys.argv).main()
