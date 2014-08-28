'''
Module with app-specific code for photo viewer.
'''
from pisak.viewer import launcher
import os.path

def prepare_photo_view(stage, script, data):
    
def prepare_album_view(stage, script, data):

def prepare_library_view(stage, script, data):

def prepare_photo_edition_view(stage, script, data):

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
