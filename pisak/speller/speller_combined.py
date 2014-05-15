from pisak import switcher_app
from gi.repository import Clutter, Mx
import sys
import pisak.speller.widgets


class PisakSpellerStage(Clutter.Stage):
    def __init__(self, context):
        super().__init__()
        self.context = context
        Mx.Button() # workaround for GI loader
        self.script = Clutter.Script()
        self.script.load_from_file("speller_combined.json")
        view_actor = self.script.list_objects()[0]
        self.add_child(view_actor)


class PisakSpellerApp(switcher_app.Application):
    """
    Pisak speller app with pisak speller stage.
    """
    def create_stage(self, argv):
        stage = PisakSpellerStage(self.context)
        #stage.set_fullscreen(True)
        return stage


if __name__ == "__main__":
    PisakSpellerApp(sys.argv).main()
