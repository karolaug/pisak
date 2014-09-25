'''
Module with app-specific code for photo viewer.
'''
from pisak.viewer import library_manager
from pisak import launcher, xdg, res
import logging


def button_to_stage(stage, script, button_name, stage_to_load, data=None):
    button = script.get_object(button_name)
    if button is not None:
        button.connect("clicked", lambda *_: stage.load_view(stage_to_load,
                                                             data))

        
def _extract_album_name(path):
    pic_dir = xdg.get_dir('pictures')
    if path == pic_dir:
        return path.split('/')[-1]
    else:        
        return path.partition(pic_dir)[-1][1:]


def prepare_photo_view(stage, script, data):
    slideshow = script.get_object("slideshow_widget")
    header = script.get_object("header")
    album = data["album"]
    if header:
        header.set_text(_extract_album_name(album))
    button_to_stage(stage, script, "button_edition", 
                    "viewer/photo_editing", {"slideshow": slideshow,
                                             "album": album})
    button_to_stage(stage, script, "button_album", "viewer/album",
                    {"album_name": album})
    button_to_stage(stage, script, "button_library", "viewer/library")
    data_source = script.get_object("photo_data_source")
    data_source.album = album
    slideshow.show_initial_slide(data_source.data.index(data["photo"]))


def prepare_album_view(stage, script, data):
    button_to_stage(stage, script, "button_library", "viewer/library")
    header = script.get_object("header")
    album = data["album_name"]
    header.set_text(_extract_album_name(album))
    library = script.get_object("library_data")
    library.tiles_handler = lambda tile, photo, album: stage.load_view("viewer/photo",
                                            {"photo": photo, "album": album})
    library.album = album
    library.album = data["album_name"]
    button_to_stage(stage, script, "button_start", "main_panel/main")


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
    button_to_stage(stage, script, "button_start", "main_panel/main")
    

VIEWS = {
    "viewer/photo": (res.get("json/viewer/photo.json"), prepare_photo_view),
    "viewer/album": (res.get("json/viewer/album.json"), prepare_album_view),
    "viewer/library": (res.get("json/viewer/library.json"), prepare_library_view),
    "viewer/photo_editing": (res.get("json/viewer/photo_editing.json"),
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
