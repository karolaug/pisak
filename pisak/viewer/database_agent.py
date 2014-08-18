import os
from datetime import datetime

from gi.repository.GExiv2 import Metadata

from pisak.database_manager import DatabaseConnector


_CREATE_PHOTOS = "CREATE TABLE IF NOT EXISTS photos ( \
                                    path TEXT, \
                                    category TEXT, \
                                    created_on TIMESTAMP, \
                                    added_on TIMESTAMP, \
                                    PRIMARY KEY (path, category))"

_CREATE_FAVOURITE_PHOTOS = "CREATE TABLE IF NOT EXISTS favourite_photos ( \
                                            id INTEGER PRIMARY KEY, \
                                            path TEXT UNIQUE, \
                                            category TEXT, \
                                            created_on TIMESTAMP, \
                                            added_on TIMESTAMP)"


def get_categories():
    db = DatabaseConnector()
    db.execute(_CREATE_PHOTOS)
    query = "SELECT DISTINCT category FROM photos"
    categories = db.execute(query)
    db.close_connection()
    return categories

def get_photos(category):
    db = DatabaseConnector()
    db.execute(_CREATE_PHOTOS)
    query = "SELECT * FROM photos WHERE category='" + category + "' ORDER BY created_on ASC, added_on ASC"
    photos = db.execute(query)
    db.close_connection()
    return photos

def get_favourite_photos():
    db = DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_PHOTOS)
    query = "SELECT * FROM favourite_photos ORDER BY id DESC, created_on ASC, added_on ASC"
    favourite_photos = db.execute(query)
    db.close_connection()
    return favourite_photos

def add_to_favourite_photos(path):
    if is_in_favourite_photos(path):
        return False
    else:
        db = DatabaseConnector()
        db.execute(_CREATE_FAVOURITE_PHOTOS)
        db.execute(_CREATE_PHOTOS)
        query = "INSERT INTO favourite_photos (path, category, created_on, added_on) \
                                                SELECT * FROM photos WHERE path='" + path + "'"
        db.execute(query)
        db.commit()
        db.close_connection()
        return True

def is_in_favourite_photos(path):
    db = DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_PHOTOS)
    query = "SELECT * FROM favourite_photos WHERE path='" + path + "'"
    favourite_photos = db.execute(query)
    db.close_connection()
    if favourite_photos:
        return True
    else:
        return False

def insert_photo(path, category):
    db = DatabaseConnector()
    db.execute(_CREATE_PHOTOS)
    meta = Metadata(path)
    if meta.has_exif():
        created_on = meta.get_date_time()
    else:
        created_on = datetime.fromtimestamp(os.path.getctime(path))
    added_on = db.generate_timestamp()
    query = "INSERT OR IGNORE INTO photos (path, category, created_on, added_on) VALUES (?, ?, ?, ?)"
    values = (path, category, created_on, added_on,)
    db.execute(query, values)
    db.commit()
    db.close_connection()

def insert_many_photos(photos_list):
    db = DatabaseConnector()
    db.execute(_CREATE_PHOTOS)
    added_on = db.generate_timestamp()
    for photo in photos_list:
        meta = Metadata(photo[0])  # photo path as the first item
        if meta.has_exif():
            photo.append(meta.get_date_time())
        else:
            photo.append(datetime.fromtimestamp(os.path.getctime(photo[0])))
        photo.append(added_on)
    query = "INSERT OR IGNORE INTO photos (path, category, created_on, added_on) VALUES (?, ?, ?, ?)"
    db.executemany(query, photos_list)
    db.commit()
    db.close_connection()

def remove_from_favourite_photos(path):
    db = DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_PHOTOS)
    query = "DELETE FROM favourite_photos WHERE path='" + path + "'"
    db.execute(query)
    db.commit()
    db.close_connection()

