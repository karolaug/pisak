import os.path
from datetime import datetime, timedelta
from time import gmtime

from gi.repository import GExiv2, GObject

from pisak import xdg
from pisak.viewer import database_agent


EPOCH = gmtime(0)


_LAST_PHOTO_ADDED_ON = database_agent.get_last_photo_insertion_time()
if _LAST_PHOTO_ADDED_ON:
    PHOTO_REF_TIME = (_LAST_PHOTO_ADDED_ON - \
                      datetime(EPOCH.tm_year, EPOCH.tm_mon,
                            EPOCH.tm_mday, EPOCH.tm_hour,
                            EPOCH.tm_min, EPOCH.tm_sec)) / \
                            timedelta(seconds=1)
else:
    PHOTO_REF_TIME = 0


_LAST_ALBUM_ADDED_ON = database_agent.get_last_album_insertion_time()
if _LAST_ALBUM_ADDED_ON:
    ALBUM_REF_TIME = (_LAST_ALBUM_ADDED_ON - \
                      datetime(EPOCH.tm_year, EPOCH.tm_mon,
                            EPOCH.tm_mday, EPOCH.tm_hour,
                            EPOCH.tm_min, EPOCH.tm_sec)) / \
                            timedelta(seconds=1)
else:
    ALBUM_REF_TIME = 0


LIBRARY_DIR = xdg.get_dir("pictures")


EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".gif", ".raw", ".bmp", ".svg")


def load_new():
    path_generator = os.walk(LIBRARY_DIR)
    for current, subdirs, files in path_generator:
        if os.path.getmtime(current) > ALBUM_REF_TIME:
            database_agent.insert_album(current)
            new_photos = []
            for photo_path in [os.path.join(current, name) for name in files]:
                if os.path.getctime(photo_path) > PHOTO_REF_TIME:
                    if os.path.splitext(photo_path)[-1].lower() in EXTENSIONS:
                        try:
                            meta = GExiv2.Metadata(photo_path)  # photo path as the first item
                            if meta.has_tag("Exif.Photo.DateTimeOriginal"):
                                created_on = meta.get_date_time()
                                if not isinstance(created_on, datetime):
                                    created_on = datetime.fromtimestamp(os.path.getctime(photo_path))
                            else:
                                created_on = datetime.fromtimestamp(os.path.getctime(photo_path))
                        except GObject.GError:
                            created_on = datetime.fromtimestamp(os.path.getctime(photo_path))
                        new_photos += [[photo_path, created_on]]
            database_agent.insert_many_photos_to_album(new_photos, current)
