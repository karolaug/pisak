"""
Module with functions for searching and loading photos and folders
from the file system's default pictures directory.
"""
import os
# import imghdr  # another possibility

from pisak import xdg


#: Path to the system's default pictures directory
LIBRARY_DIR = xdg.get_dir("pictures")


#: Extensions of the supported file formats
EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".gif", ".raw", ".bmp")


def get_all_albums():
    """
    Return the list of folders from inside the default directory
    """
    return [item[0] for item in os.walk(LIBRARY_DIR)]


def get_photos_from_album(album):
    """
    Return the list of files in the given folder whose names fullfill
    the extensions' condition
    :param album: path to the folder
    """
    return [os.path.join(album, file) for file in os.listdir(album) if
            os.path.splitext(file)[-1].lower() in EXTENSIONS]


def get_preview_of_album(album):
    """
    Return the path to the first file in the given folder whose name fullfill
    the extensions' condition, or None
    :param album: path to the folder
    """
    for file in os.listdir(album):
        if os.path.splitext(file)[-1].lower() in EXTENSIONS:
            return os.path.join(album, file)
