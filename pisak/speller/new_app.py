from pisak import switcher_app
from gi.repository import Clutter
import sys


class PisakSpellerStage(Clutter.Stage):
    def __init__(self, context):
        self.context = context
        self.script = Clutter.Script()
        self.script.load_from_file("speller_view.json")
        view_actor = self.script.list_objects()[0]
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
