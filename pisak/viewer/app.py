'''
Module with app-specific code for photo viewer.
'''
import os

from pisak.viewer import library_manager
from pisak import launcher


def button_to_stage(stage, script, button_name, stage_to_load, data=None):
    button = script.get_object(button_name)
    button.connect("clicked", lambda *_: stage.load_view(stage_to_load, data))


def prepare_photo_view(stage, script, data):

    slideshow = script.get_object("slideshow_widget")
    button_to_stage(stage, script, "button_edition",
                    "viewer/photo_editing", {"slideshow": slideshow,
                                      "album": data["album"]})
    button_to_stage(stage, script, "button_album", "viewer/album",
                    {"album_name": data["album"]})
    button_to_stage(stage, script, "button_library", "viewer/library")
    data_source = script.get_object("photo_data_source")
    data_source.album = data["album"]  # data["album_name"]
    slideshow.show_initial_slide(data_source.data.index(data["photo"]))  # data["index"]



def prepare_album_view(stage, script, data):
    button_to_stage(stage, script, "button_library", "viewer/library")
    library = script.get_object("library_data")
    library.tiles_handler = lambda tile, photo, album: stage.load_view(
        "viewer/photo", {"photo": photo, "album": album})
    library.album = data["album_name"]
    button_to_stage(stage, script, "button_start", "main_panel/main")
    button_to_stage(stage, script, "button_start", "photo") # -> start panel


def prepare_library_view(stage, script, data):
    library_data = script.get_object("library_data")
    library_data.tiles_handler = lambda tile, album: stage.load_view(
        "viewer/album", {"album_name": album})
    button_to_stage(stage, script, "button_start", "main_panel/main")


def prepare_photo_editing_view(stage, script, data):
    photo = script.get_object("slide")
    photo.photo_path = data["slideshow"].slide.photo_path
    button_to_stage(stage, script, "button_photo", "viewer/photo",
                        {"photo": photo.photo_path, "album": data["album"]})


def _fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)


VIEWS = {
    "viewer/photo": (_fix_path("photo.json"), prepare_photo_view),
    "viewer/album": (_fix_path("album.json"), prepare_album_view),
    "viewer/library": (_fix_path("library.json"), prepare_library_view),
    "viewer/photo_editing": (_fix_path("photo_editing.json"),
                        prepare_photo_editing_view)
}


if __name__ == "__main__":
    _viewer_app = {
        "views": VIEWS,
        "initial-view": "viewer/library",
        "initial-data": None
    }
    launcher.run(_viewer_app)
