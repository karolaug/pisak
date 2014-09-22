'''
Module with app-specific code for photo viewer.
'''
import os

#from pisak.viewer import library_manager
from pisak import launcher, xdg
import logging
from pisak.viewer import model


def button_to_stage(stage, script, button_name, stage_to_load, data=None):
    button = script.get_object(button_name)
    if button is not None:
        button.connect("clicked", lambda *_: stage.load_view(stage_to_load,
                                                             data))


def prepare_photo_view(stage, script, data):
    album_id = data["album_id"]
    photo_id = data["photo_id"]

    data_source = script.get_object("photo_data_source")
    data_source.album = album_id

    slideshow = script.get_object("slideshow_widget")
    slideshow.show_initial_photo_id(photo_id)

    button_to_stage(
        stage, script, "button_edition", "viewer/photo_editing",
        {"album_id": album_id})

    button_to_stage(
        stage, script, "button_album", "viewer/album", {"album_id": album_id})
    button_to_stage(stage, script, "button_library", "viewer/library")

    library = model.get_library()
    header = script.get_object("header")
    header.set_text(library.get_category_by_id(album_id).name)


def prepare_album_view(stage, script, data):
    album_id = data["album_id"]

    button_to_stage(stage, script, "button_library", "viewer/library")
    button_to_stage(stage, script, "button_start", "main_panel/main")

    library = model.get_library()
    header = script.get_object("header")
    header.set_text(library.get_category_by_id(album_id).name)

    data_source = script.get_object("library_data")
    def photo_tile_handler(tile, photo_id, album_id):
        stage.load_view(
            "viewer/photo", {"photo_id": photo_id, "album_id": album_id})
    data_source.tiles_handler = photo_tile_handler
    data_source.album = album_id


def prepare_library_view(stage, script, data):
    library_data = script.get_object("library_data")
    library_data.tiles_handler = lambda tile, album: stage.load_view(
        "viewer/album", {"album_id": album})
    button_to_stage(stage, script, "button_start", "main_panel/main")


def prepare_photo_editing_view(stage, script, data):
    photo = script.get_object("slide")
    photo.photo_path = data["slideshow"].slide.photo_path
    button_to_stage(stage, script, "button_photo", "viewer/photo",
                        {"photo_id": photo.id, "album_id": data["album_id"]})
    button_to_stage(stage, script, "button_start", "main_panel/main")
    

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
    logging.basicConfig(level=logging.DEBUG)
    _viewer_app = {
        "views": VIEWS,
        "initial-view": "viewer/library",
        "initial-data": None
    }
    launcher.run(_viewer_app)
