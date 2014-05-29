import sys, os.path

from gi.repository import Clutter, Mx

from pisak import switcher_app, res

import pisak.speller.widgets  # @UnusedImport
import pisak.layout  # @UnusedImport


class PisakSpellerStage(Clutter.Stage):
    SCRIPT_PATH = "speller_combined.json"
    STYLE_PATH = os.path.join(res.PATH, "photo_edit.css")

    def __init__(self, context):
        super().__init__()
        self.context = context
        self.style = Mx.Style.get_default()
        self.style.load_from_file(self.STYLE_PATH)
        self._load_script()

    def _load_script(self):
        Mx.Button() # workaround for GI loader
        self.script = Clutter.Script()
        self.script.load_from_file(self.SCRIPT_PATH)
        self.view_actor = self.script.get_object("main")
        self.text_box = self.script.get_object("text_box")
        self.text_box.get_children()[0].set_property('line-wrap', True)
        print(self.text_box.get_children()[0].get_property('line-wrap'))
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
