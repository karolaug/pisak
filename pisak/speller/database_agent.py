import os
import sqlite3
from datetime import datetime

def insert_text_file(name):
    db = SpellerDatabaseConnector()
    db.insert_text_file(name)
    db.commit()
    db.close_connection()

def get_text_files():
    db = SpellerDatabaseConnector()
    text_files = db.get_all_records()
    db.close_connection()
    return text_files

def get_text_file_path(name):
    db = SpellerDatabaseConnector()
    path = db.get_file_path(name)
    db.close_connection()
    return path


class SpellerDatabaseConnector(object):
    DB_PATH = os.path.join(os.path.abspath(os.path.split(__file__)[0]),
                           "speller_database.db")
    TABLE_NAME = "text_files"
    FILE_PATH_BASE = os.path.abspath(os.path.split(__file__)[0])
    FILE_NAME_BASE = "text_file_no_"
    FILE_NAME_SUFFIX = ".txt"
    def __init__(self):
        self._open_connection()
        self._create_table()

    def insert_text_file(self, name):
        query = "INSERT INTO " + self.TABLE_NAME + " VALUES (?, ?, ?)"
        values = (self._generate_path(), name, self._generate_timestamp(),)
        self._execute(query, values)

    def get_all_records(self):
        query = "SELECT * FROM " + self.TABLE_NAME
        return self._execute(query)

    def get_file_path(self, name):
        query = "SELECT path FROM " + self.TABLE_NAME + " WHERE name=?"
        return self._execute(query, (name,))[0][0]

    def commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def _open_connection(self):
        self.conn = sqlite3.connect(self.DB_PATH,
                                    detect_types=sqlite3.PARSE_DECLTYPES|
                                    sqlite3.PARSE_COLNAMES)

    def _execute(self, query, values=None):
        cur = self.conn.cursor()
        if values:
            cur.execute(query, values)
        else:
            cur.execute(query)
        return cur.fetchall()

    def _get_table_length(self):
        query = "SELECT COUNT(*) FROM " + self.TABLE_NAME
        return self._execute(query)[0][0]

    def _create_table(self):
        query = "CREATE TABLE IF NOT EXISTS " + self.TABLE_NAME \
                + "(path TEXT, name TEXT, created TIMESTAMP)"
        self._execute(query)

    def _generate_timestamp(self):
        return datetime.now()

    def _generate_path(self):
        file_no = self._get_table_length() + 1
        file_name = self.FILE_NAME_BASE + str(file_no) + self.FILE_NAME_SUFFIX
        return os.path.join(self.FILE_PATH_BASE, file_name)
