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
                    "photo_editing", {"slideshow": slideshow})
    button_to_stage(stage, script, "button_album", "album")

    button_to_stage(stage, script, "button_library", "library")

    # button_to_stage(stage, script, "button_start", "start") -> start panel
    data_source = script.get_object("photo_data_source")
    data_source.album = library_manager.LIBRARY_DIR  # data["album_name"]
    slideshow.show_initial_slide(0)  # data["index"]



def prepare_album_view(stage, script, album_name):

    button_to_stage(stage, script, "button_library", "library")

    library = script.get_object("library_data")
    # for index, photo in enumerate(library.tiles):
        # photo.connect("clicked", lambda *_: stage.load_view(
                                                    #"photo",
                                                    #{"index": index,
                                                    #"album": data["album_name"]}))

    album = script.get_object("library_data")
    album.album = library_manager.LIBRARY_DIR  # data["album_name"]  # also through set property should page the new album

    # also through set property should page the new album

    button_to_stage(stage, script, "button_start", "photo") # -> start panel

def prepare_library_view(stage, script, data):

    #button_to_stage(stage, script, "button_library", "library")

    library = script.get_object("library_data")
    # for album in library.data:
        # album.connect("activate", lambda *_:
        #stage.load_view("album", {"album_name": album["category"]}))

    button_to_stage(stage, script, "button_start", "photo") # -> start panel


def prepare_photo_editing_view(stage, script, data):
    photo = script.get_object("slide")
    photo.photo_path = data["slideshow"].slide.photo_path

    button = script.get_object("button_photo")
    button.connect("clicked", lambda *_: stage.load_view("photo", photo))

    # button_to_stage(stage, script, "button_start", "start") -> start panel


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
    "initial-view": "photo",
    "initial-data": None
}


if __name__ == "__main__":
    launcher.run(VIEWER_APP)
