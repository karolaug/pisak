import os

from pisak.database_manager import DatabaseConnector


_FILE_PATH_BASE = os.getenv("HOME")

_FILE_NAME_BASE = "text_file_no_"

_FILE_NAME_SUFFIX = ".txt"

_CREATE_TEXT_FILES = "CREATE TABLE IF NOT EXISTS text_files( \
                                        id INTEGER PRIMARY KEY, \
                                        path TEXT, \
                                        name TEXT, \
                                        added_on TIMESTAMP)"


def insert_text_file(name):
    db = DatabaseConnector()
    db.execute(_CREATE_TEXT_FILES)
    path = _generate_new_path(db)
    added_on = db.generate_timestamp()
    query = "INSERT INTO text_files (path, name, added_on) VALUES (?, ?, ?)"
    values = (path, name, added_on,)
    db.execute(query, values)
    db.commit()
    db.close_connection()
    return path

def get_text_files():
    db = DatabaseConnector()
    db.execute(_CREATE_TEXT_FILES)
    query = "SELECT * FROM text_files"
    text_files = db.execute(query)
    db.close_connection()
    return text_files

def _generate_new_path(db):
    _query = "SELECT COUNT(*) FROM text_files"
    file_no = db.execute(_query)[0][0] + 1
    file_name = _FILE_NAME_BASE + str(file_no) + _FILE_NAME_SUFFIX
    return os.path.join(_FILE_PATH_BASE, file_name)
