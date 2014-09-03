'''
Module with app-specific code for photo viewer.
'''
from pisak import launcher
import os

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
    data_source.album = os.getenv("HOME")  # data["album_name"]
    slideshow.show_initial_slide(0)  # data["index"]

def prepare_album_view(stage, script, data):

    button_to_stage(stage, script, "button_library", "library")

    library = script.get_object("library_data")
    #for index, photo in enumerate(library.tiles):
        #photo.connect("activate", lambda *_: stage.load_view(
                                                    #"photo",
                                                    #{"index": index,
                                                    #"album": data["album_name"]}))

    album = script.get_object("library_data")
    album.album = None  # data["album_name"]  # also through set property should page the new album
    

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
    print(VIEWER_APP)
    launcher.run(VIEWER_APP)
