import os.path
import sqlite3

LIBRARY_FILENAME = ".pisak_view.db"

def create_library(path):
    db_file = os.path.join(path, LIBRARY_FILENAME)
    if os.path.exists(db_file):
        raise LibraryException("Library already exists")
    return Library(path)
    
class LibraryException(Exception):
    pass


class 

class Category(object):
    pass

class Library(object):
    def __init__(self, path):
        self.path = path
        self.db_file = os.path.join(path, LIBRARY_FILENAME)
        self.db_connection = sqlite3.connect(self.db_file)
    
    @property
    def categories(self):
        return []
    
    def scan(self):
        pass
    
    def close(self):
        self.db_connection.close()


