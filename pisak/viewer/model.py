import os.path
from pisak import xdg
import magic

ACCEPTED_TYPES = [
    "image/png", "image/jpeg", "image/x-ms-bmp", "image/gif", "image/svg+xml"]


LIBRARY_DIR = xdg.get_dir("pictures")

_LIBRARY_STORE = {}

class LibraryException(Exception):
    pass


class Category(object):
    def __init__(self, album_id, name):
        self.id = album_id
        self.name = name
        self.photos = []
    
    def get_preview_path(self):
        photo = self.photos[0].path
        return photo


class Photo(object):
    def __init__(self, path):
        self.path = path


class Library(object):
    def __init__(self, path):
        self.path = path
        #self.library_dir = os.path.join(path, LIBRARY_SUBDIR)
        self.categories = set()
        self.photos = set()

    def scan(self):
        scanner = Scanner(self)
        return scanner.scan()

    def add_category_photo(self, category, photo):
        self.categories.add(category)
        self.photos.add(photo)
        category.photos.append(photo)
    
    def get_category_by_id(self, category_id):
        for category in self.categories:
            if category.id == category_id:
                return category
        raise LibraryException("No such category id")

    def close(self):
        pass


class Scanner(object):
    def __init__(self, library):
        self.library = library
        self.magic = magic.open(magic.MIME_TYPE | magic.SYMLINK)
        self.magic.load()

    def get_photo_paths(self):
        return set([photo.path for photo in self.library.photos])

    def scan(self):
        """
        Scan library directory for new photos. Return a list of newly imported photo objects.
        """
        all_photos = []
        new_photos = set()
        old_photos = self.get_photo_paths()
        next_id = 0
        path_generator = os.walk(self.library.path)
        for current, _subdirs, files in path_generator:
            if current.startswith("."):
                continue
            new_category = Category(next_id, current)
            next_id += 1
            for photo_path in [os.path.join(current, name) for name in files]:
                if self._test_file(photo_path):
                    all_photos.append([photo_path, current])
                    if photo_path in old_photos:
                        continue
                    new_photo = Photo(photo_path)
                    self.library.add_category_photo(new_category, new_photo)
                    new_photos.add(new_photo)
        return new_photos, all_photos
    
    def _test_file(self, path):
        file_type = self.magic.file(path)
        return file_type in ACCEPTED_TYPES
            
        


def get_library(base_path=None):
    if base_path is None:
        base_path = LIBRARY_DIR
    try:
        library = _LIBRARY_STORE[base_path]
    except KeyError:
        library = Library(base_path)
        library.scan()
        _LIBRARY_STORE[base_path] = library
    return library
