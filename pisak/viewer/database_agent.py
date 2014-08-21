import os
from datetime import datetime

from gi.repository import GExiv2, GObject

from pisak.database_manager import DatabaseConnector


_CREATE_PHOTOS = "CREATE TABLE IF NOT EXISTS photos ( \
                                    id INTEGER PRIMARY KEY, \
                                    path TEXT NOT NULL, \
                                    category TEXT NOT NULL, \
                                    created_on TIMESTAMP NOT NULL, \
                                    added_on TIMESTAMP NOT NULL, \
                                    UNIQUE (path, category))"

_CREATE_FAVOURITE_PHOTOS = "CREATE TABLE IF NOT EXISTS favourite_photos ( \
                                            id INTEGER PRIMARY KEY, \
                                            path TEXT UNIQUE NOT NULL REFERENCES photos(path), \
                                            category TEXT NOT NULL REFERENCES photos(category))"



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

def get_previews(categories_list):
    db = DatabaseConnector()
    db.execute(_CREATE_PHOTOS)
    previews = {}
    query = "SELECT * FROM photos WHERE category='{}' ORDER BY created_on DESC, added_on DESC LIMIT 1"
    for category in categories_list:
        previews[category] = db.execute(query.format(category))[0]
    db.close_connection()
    return previews

def get_favourite_photos():
    db = DatabaseConnector()
    db.execute(_CREATE_FAVOURITE_PHOTOS)
    query = "SELECT favs.id, favs.path, favs.category, created_on, added_on FROM favourite_photos AS favs JOIN \
                photos ON photos.path=favs.path AND photos.category=favs.category ORDER BY favs.id DESC, created_on ASC, added_on ASC"
    favourite_photos = db.execute(query)
    db.close_connection()
    return favourite_photos

def add_to_favourite_photos(path, category):
    if is_in_favourite_photos(path):
        return False
    else:
        db = DatabaseConnector()
        db.execute(_CREATE_FAVOURITE_PHOTOS)
        db.execute(_CREATE_PHOTOS)
        values = (path, category,)
        query = "INSERT INTO favourite_photos (path, category) VALUES (?, ?)"
        db.execute(query, values)
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
    try:
        meta = GExiv2.Metadata(path)
        if meta.has_tag("Exif.Photo.DateTimeOriginal"):
            created_on = meta.get_date_time()
        else:
            created_on = datetime.fromtimestamp(os.path.getctime(path))
    except GObject.GError:
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
        try:
            meta = GExiv2.Metadata(photo[0])  # photo path as the first item
            if meta.has_tag("Exif.Photo.DateTimeOriginal"):
                photo.append(meta.get_date_time())
            else:
                photo.append(datetime.fromtimestamp(os.path.getctime(photo[0])))
        except GObject.GError:
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

