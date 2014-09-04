import os

from pisak import xdg


LIBRARY_DIR = xdg.get_dir("pictures")


EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".gif", ".raw", ".bmp")


def get_all_albums():
    return [item[0] for item in os.walk(LIBRARY_DIR)]


def get_photos_from_album(album):
    return [os.path.join(album, file) for file in os.listdir(album) if os.path.splitext(file)[-1].lower()
            in EXTENSIONS]


def get_preview_of_album(album):
    return get_photos_from_album(album)[0]
