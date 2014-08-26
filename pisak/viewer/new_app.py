import os.path

from gi.repository import Clutter, Mx

from pisak import res, widgets, layout
import pisak.viewer.widgets


_PATH = os.path.abspath(os.path.split(__file__)[0])


def _local_get(relative):
    return os.path.join(_PATH, relative)


VIEWS = {
    "album": {
        "path": _local_get("album.json")
    },
    "library": {
        "path": _local_get("library.json")
    },
    "photo": {
        "path": _local_get("photo.json")
    }
}


if __name__ == "__main__":
    Clutter.init([])
    stage = Clutter.Stage()
    Mx.Style.get_default().load_from_file(os.path.join(res.PATH, "css/viewer.css"))
    stage.set_fullscreen(True)
    script = Clutter.Script()
    script.load_from_file(VIEWS["library"]["path"])
    main = script.get_object("main")
    stage.add_child(main)
    stage.connect("destroy", lambda _: Clutter.main_quit())
    stage.show_all()
    Clutter.main()
