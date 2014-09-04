"""
Module for loading informations about photos stored in the file system
and passing them to photos specific database.
"""
import os.path
from datetime import datetime, timedelta
from time import gmtime

from gi.repository import GExiv2, GObject

from pisak import xdg
from pisak.viewer import database_agent


EPOCH = gmtime(0)


def _datetime_to_float(dttime):
    return (dttime - datetime(EPOCH.tm_year, EPOCH.tm_mon,
                            EPOCH.tm_mday, EPOCH.tm_hour,
                            EPOCH.tm_min, EPOCH.tm_sec)) / \
                            timedelta(seconds=1)


PHOTO_REF_TIME = _datetime_to_float(
    database_agent.get_last_photo_insertion_time())


ALBUM_REF_TIME = _datetime_to_float(
    database_agent.get_last_album_insertion_time())


REF_TIME = database_agent.get_db_last_modification_time()


LIBRARY_DIR = xdg.get_dir("pictures")


EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".gif", ".raw", ".bmp")


def load_new():
    if database_agent.is_db_empty():
        _load_new_since()
    else:
        _load_new_since(REF_TIME)


def _get_photo_creation_time(photo_path):
    try:
        meta = GExiv2.Metadata(photo_path)
        if meta.has_tag("Exif.Photo.DateTimeOriginal"):
            created_on = meta.get_date_time()
            if not isinstance(created_on, datetime):
                created_on = datetime.fromtimestamp(os.path.getctime(photo_path))
        else:
            created_on = datetime.fromtimestamp(os.path.getctime(photo_path))
    except GObject.GError:
        created_on = datetime.fromtimestamp(os.path.getctime(photo_path))
    return created_on


def _load_new_since(ref_time=0):
    path_generator = os.walk(LIBRARY_DIR)
    for current, _subdirs, files in path_generator:
        if os.path.getmtime(current) > ref_time:
            database_agent.insert_album(current)
            new_photos = []
            for photo_path in [os.path.join(current, name) for name in files]:
                if (os.path.getctime(photo_path) > ref_time and 
                        os.path.splitext(photo_path)[-1].lower() in EXTENSIONS):
                    created_on = _get_photo_creation_time(photo_path)
                    new_photos.append([photo_path, created_on])
            database_agent.insert_many_photos_to_album(new_photos, current)
