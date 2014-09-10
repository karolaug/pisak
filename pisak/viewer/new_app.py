import os.path
import sys

from gi.repository import Clutter, Mx

from pisak import switcher_app, signals, res, pager
from pisak.viewer import widgets, model, database_agent, handlers


_LIBRARY_PATH = os.getenv("HOME")
_MODULE_PATH = os.path.abspath(os.path.split(__file__)[0])


def _local_get(relative):
    return os.path.join(_MODULE_PATH, relative)


VIEWS = {
    "album": {
        "path": _local_get("album.json")
    },
    "library": {
        "path": _local_get("library.json")
    },
    "photo": {
        "path": _local_get("photo.json")
    },
    "photo_edition": {
        "path": _local_get("photo_edition.json")
    }
}


class PisakViewerStage(Clutter.Stage):
    STYLESHEET_PATH = os.path.join(res.PATH, "css/viewer.css")

    def __init__(self, context, script_path):
        super().__init__()
        self.context = context
        self.script_path = script_path
        self._load_script()
        self._load_stylesheet()

    def _load_script(self):
        self.script = Clutter.Script()
        self.script.load_from_file(self.script_path)
        self.script.connect_signals_full(signals.connect_registered)
        self.view_actor = self.script.get_object("main")
        self.set_layout_manager(Clutter.BinLayout())
        self.add_child(self.view_actor)

    def _load_stylesheet(self):
        Mx.Style.get_default().load_from_file(self.STYLESHEET_PATH)


class PisakViewerApp(switcher_app.Application):
    """
    Pisak viewer app with pisak speller stage.
    """
    def create_stage(self, argv):
        script_path = VIEWS[argv[1]]["path"]
        stage = PisakViewerStage(self.context, script_path)
        stage.set_size(1366, 768)
        stage.set_fullscreen(True)
        return stage


def generate_viewer_data():
    model.LIBRARY_SUBDIR = ""
    lib = model.Library(_LIBRARY_PATH)
    all_photos = lib.scan()[-1]
    database_agent.insert_many_photos(all_photos)

    
def usage():
    print("Usage: new_app.py VARIANT")
    print(
        "Where variant is on of:\n"
        "  album\n"
        "  library\n"
        "  photo\n"
        "  photo_edition")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    elif sys.argv[1] not in VIEWS:
        usage()
    else:
        generate_viewer_data()
        PisakViewerApp(sys.argv).main()
