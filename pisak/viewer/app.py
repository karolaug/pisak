'''
Module with app-specific code for photo viewer.
'''
import os

from pisak.viewer import library_manager
from pisak import launcher


def button_to_stage(stage, script, button_name, stage_to_load, data=None):
    button = script.get_object(button_name)
    if button is not None:
        button.connect("clicked", lambda *_: stage.load_view(stage_to_load,
                                                             data))


def prepare_photo_view(stage, script, data):
    slideshow = script.get_object("slideshow_widget")
    button_to_stage(stage, script, "button_edition", 
                    "photo_editing", {"slideshow": slideshow,
                                      "album": data["album"]})
    button_to_stage(stage, script, "button_album", "album",
                    {"album_name": data["album"]})
    button_to_stage(stage, script, "button_library", "library")
    data_source = script.get_object("photo_data_source")
    data_source.album = data["album"]
    slideshow.show_initial_slide(data_source.data.index(data["photo"]))


def prepare_album_view(stage, script, data):
    button_to_stage(stage, script, "button_library", "library")
    library = script.get_object("library_data")
    library.tiles_handler = lambda tile, photo, album: stage.load_view("photo",
                                            {"photo": photo, "album": album})
    library.album = data["album_name"]
    # start panel:
    # button_to_stage(stage, script, "button_start", "start_panel")


def prepare_library_view(stage, script, data):
    library_data = script.get_object("library_data")
    library_data.tiles_handler = lambda tile, album: stage.load_view(
        "album", {"album_name": album})
    # start panel:
    # button_to_stage(stage, script, "button_start", "start_panel")


def prepare_photo_editing_view(stage, script, data):
    photo = script.get_object("slide")
    photo.photo_path = data["slideshow"].slide.photo_path
    button = script.get_object("button_photo")
    button.connect("clicked", lambda *_: stage.load_view("photo",
                        {"photo": photo.photo_path, "album": data["album"]}))


def fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)


VIEWER_APP = {
    "views": {
        "photo": (fix_path("photo.json"), prepare_photo_view),
        "album": (fix_path("album.json"), prepare_album_view),
        "library": (fix_path("library.json"), prepare_library_view),
        "photo_editing": (fix_path("photo_editing.json"),
                          prepare_photo_editing_view),
    },
    "initial-view": "library",
    "initial-data": None
}


if __name__ == "__main__":
    launcher.run(VIEWER_APP)
