'''
Module with app-specific code for photo viewer.
'''
import os

from gi.repository import GLib

from pisak.viewer import launcher, model, database_agent


_LIBRARY_PATH = GLib.get_user_special_dir(GLib.USER_DIRECTORY_PICTURES)


def button_to_stage(stage, script, button_name, stage_to_load, data=None):
    button = script.get_object(button_name)
    button.connect("activate", lambda *_: stage.load_view(stage_to_load, data))


def prepare_photo_view(stage, script, data):

    slideshow = script.get_object("slideshow_widget")
    button_to_stage(stage, script, "button_edition", "photo_edition", {"slideshow": slideshow})

    button_to_stage(stage, script, "button_album", "album")

    button_to_stage(stage, script, "button_library", "library")

    #button_to_stage(stage, script, "button_start", "start") -> start panel
    data_source = script.get_object("photo_data_source")
    data_source.album = _LIBRARY_PATH  # data["album_name"]
    slideshow.show_initial_slide(None)  # data["index"]
    

def prepare_album_view(stage, script, album_name):

    button_to_stage(stage, script, "button_library", "library")

    library = script.get_object("library_data")
    #for index, photo in enumerate(library.tiles):
        #photo.connect("activate", lambda *_: stage.load_view(
                                                    #"photo",
                                                    #{"index": index,
                                                    #"album": data["album_name"]}))

    library.album = album_name
    # also through set property should page the new album

    # button_to_stage(stage, script, "button_start", "start") -> start panel


def prepare_library_view(stage, script, data):

    #button_to_stage(stage, script, "button_library", "library")

    library = script.get_object("library_data")
    #for album in library.data:
        #album.connect("activate", lambda *_: stage.load_view("album", {"album_name": album["category"]}))


    # button_to_stage(stage, script, "button_start", "start") -> start panel


def prepare_photo_edition_view(stage, script, data):

    
    photo = script.get_object("slide")
    photo.photo_path = data["slideshow"].slide.photo_path

    button = script.get_object("button_photo")
    button.connect("activate", lambda *_: stage.load_view("photo", photo))

    # button_to_stage(stage, script, "button_start", "start") -> start panel


def fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)


def generate_viewer_data():
    model.LIBRARY_SUBDIR = ""
    lib = model.Library(_LIBRARY_PATH)
    all_photos = lib.scan()[-1]
    database_agent.insert_many_photos(all_photos)
    

VIEWER_APP = {
    "views": {
        "photo": (fix_path("photo.json"), prepare_photo_view),
        "album": (fix_path("album.json"), prepare_album_view),
        "library": (fix_path("library.json"), prepare_library_view),
        "photo_edition": (fix_path("photo_edition.json"),
                          prepare_photo_edition_view),
    },
    "initial-view": "photo",
    "initial-data": None
}


if __name__ == "__main__":
    generate_viewer_data()
    launcher.run(VIEWER_APP)
