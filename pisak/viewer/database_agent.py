from gi.repository.GExiv2 import Metadata

from pisak.database_manager import DatabaseConnector


_CREATE_PHOTOS = "CREATE TABLE IF NOT EXISTS photos ( \
                                    id INTEGER PRIMARY KEY, \
                                    path TEXT, \
                                    category TEXT, \
                                    created_on TIMESTAMP, \
                                    added_on TIMESTAMP)"

_CREATE_FAVOURITE_PHOTOS = "CREATE TABLE IF NOT EXISTS favourite_photos ( \
                                            id INTEGER PRIMARY KEY, \
                                            photos_id INTEGER, \
                                            path TEXT, \
                                            category TEXT, \
                                            created_on TIMESTAMP, \
                                            added_on TIMESTAMP)"


def get_categories():
    db = DatabaseConnector()
    db.execute_query(_CREATE_PHOTOS)
    query = "SELECT DISTINCT category FROM photos"
    categories = db.execute_query(query)
    db.close_connection()
    return categories

def get_photos(category):
    db = DatabaseConnector()
    db.execute_query(_CREATE_PHOTOS)
    query = "SELECT * FROM photos WHERE category=" + category + " ORDER BY created_on ASC, added_on ASC"
    photos = db.execute_query(query)
    db.close_connection()
    return photos

def get_favourite_photos():
    db = DatabaseConnector()
    db.execute_query(_CREATE_FAVOURITE_PHOTOS)
    query = "SELECT * FROM favourite_photos ORDER BY id DESC, created_on ASC, added_on ASC"
    favourite_photos = db.execute_query(query)
    db.close_connection()
    return favourite_photos

def add_to_favourite_photos(path):
    db = DatabaseConnector()
    db.execute_query(_CREATE_FAVOURITE_PHOTOS)
    db.execute_query(_CREATE_PHOTOS)
    query = "INSERT INTO favourite_photos (photos_id, path, category, created_on, added_on) \
                                            SELECT * FROM photos WHERE path=" + path
    db.execute_query(query)
    db.commit()
    db.close_connection()

def insert_photo(path, category):
    db = DatabaseConnector()
    created_on = Metadata(path).get_date_time()
    added_on = db.generate_timestamp()
    db.execute_query(_CREATE_PHOTOS)
    query = "INSERT INTO photos (path, category, created_on, added_on) VALUES (?, ?, ?, ?)"
    values = (path, category, created_on, added_on,)
    db.execute_query(query, values)
    db.commit()
    db.close_connection()

def remove_from_favourite_photos(path):
    db = DatabaseConnector()
    db.execute_query(_CREATE_FAVOURITE_PHOTOS)
    query = "DELETE FROM favourite_photos WHERE path=" + path
    db.execute_query(query)
    db.commit()
    db.close_connection()

