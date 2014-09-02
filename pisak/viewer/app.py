'''
Module with app-specific code for photo viewer.
'''
from pisak import launcher
import os.path


def button_to_stage(stage, script, button_name, stage_to_load):
    button = script.get_object(button_name)
    button.connect("activate",
                   lambda *_: stage.load_view(stage_to_load, button))


def prepare_photo_view(stage, script, photo):

    button_to_stage(stage, script, "button_edition", "photo_edition")

    button_to_stage(stage, script, "button_album", "album")

    button_to_stage(stage, script, "button_library", "library")

    # button_to_stage(stage, script, "button_start", "start") -> start panel

    photo = script.get_object("slide")
    photo.set_property("photo_path", photo.photo_path)
    # setter should set the pic


def prepare_album_view(stage, script, album_name):

    button_to_stage(stage, script, "button_library", "library")

    library = script.get_object("library_data")
    for photo in library.tiles:
        photo.connect("activate", lambda *_: stage.load_view("photo", photo))

    album = script.get_object("library_data")
    album.album = album_name
    # also through set property should page the new album

    # button_to_stage(stage, script, "button_start", "start") -> start panel


def prepare_library_view(stage, script, data):

    button_to_stage(stage, script, "button_library", "library")

    for album in library.tiles:
        album.connect("activate", lambda *_: stage.load_view("album", album))

    # button_to_stage(stage, script, "button_start", "start") -> start panel


def prepare_photo_edition_view(stage, script, data):

    photo = script.get_object("slide")

    button = script.get_object("button_photo")
    button.connect("activate", lambda *_: stage.load_view("photo", photo))

    # button_to_stage(stage, script, "button_start", "start") -> start panel


def fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)

VIEWER_APP = {
    "views": {
        "photo": (fix_path("photo.json"), prepare_photo_view),
        "album": (fix_path("album.json"), prepare_album_view),
        "library": ("library.json", prepare_library_view),
        "photo_edition": (fix_path("photo_edition.json"),
                          prepare_photo_edition_view),
    },
    "initial-view": "photo",
    "initial-data": None
}


if __name__ == "__main__":
    launcher.run(VIEWER_APP)
