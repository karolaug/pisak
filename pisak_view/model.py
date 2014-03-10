import os.path
import os

LIBRARY_SUBDIR = ".pisak_view"

def create_library(path):
    library_dir = os.path.join(path, LIBRARY_SUBDIR)
    if os.path.exists(library_dir):
        raise LibraryException("Library already exists")
    os.mkdir(library_dir)
    return Library(path)
    
class LibraryException(Exception):
    pass

class Category(object):
    def __init__(self, name):
        self.name = name
        self.photos = set()


class Photo(object):
    def __init__(self, path):
        self.path = path


class Library(object):
    def __init__(self, path):
        self.path = path
        self.library_dir = os.path.join(path, LIBRARY_SUBDIR)
        self.categories = set()
        self.photos = set()
    
    def scan(self):
        scanner = Scanner(self)
        return scanner.scan()
    
    def add_category_photo(self, category, photo):
        self.categories.add(category)
        self.photos.add(photo)
        category.photos.add(photo)
    
    def close(self):
        pass
        
class Scanner(object):
    def __init__(self, library):
        self.library = library
    
    def get_photo_paths(self):
        return set([photo.path for photo in self.library.photos])
    
    def scan(self):
        """
        Scan library directory for new photos. Return a list of newly imported photo objects.
        """
        new_photos = set()
        old_photos = self.get_photo_paths()
        path_generator = os.walk(self.library.path)
        first_level = True
        for current, subdirs, files in path_generator:
            new_category = Category(current)
            if first_level:
                subdirs.remove(LIBRARY_SUBDIR)
                first_level = False
            for photo_path in [os.path.join(current, name) for name in files]:
                if photo_path in old_photos:
                    continue
                new_photo = Photo(photo_path)
                self.library.add_category_photo(new_category, new_photo)
                new_photos.add(new_photo)
        return new_photos

