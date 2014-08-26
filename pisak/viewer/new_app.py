import os.path

from gi.repository import Clutter, Mx


_PATH = os.path.abspath(os.path.split(__file__)[0])


def _local_get(relative):
    return os.path.join(_PATH, relative)


VIEWS = {
    "album": {
        "path": _local_get("album.json")
    }
    "library": {
        "path": _local_get("library.json")
    }
    "photo": {
        "path": _loacl_get("photo.json")
    }
}
