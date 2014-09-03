import os.path

from pisak import xdg
from pisak.viewer import database_agent
from datetime import datetime, timedelta
from time import gmtime


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


def get_new_library_items():
    new_folders = []
    new_photos = []
    path_generator = os.walk(LIBRARY_DIR)
    for current, subdirs, files in path_generator:
        if os.path.getmtime(current) > ALBUM_REF_TIME:
            new_folders.append(current)
            for photo_path in [os.path.join(current, name) for name in files]:
                if os.path.getctime(photo_path) > PHOTO_REF_TIME:
                    if os.path.splitext(photo_path)[-1].lower() in EXTENSIONS:
                        new_photos.append([photo_path, current])
    return new_folders, new_photos
