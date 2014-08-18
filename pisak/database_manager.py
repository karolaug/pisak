import os
import sqlite3
from datetime import datetime


_PATH = os.path.abspath(os.path.split(__file__)[0])

DATABASE_PATH = os.path.join(_PATH, "pisak_database.db")

CONST_APP = {
    "TABLE_NAME": {
        "speller": "text_files"
        },
    "TABLE_COLUMNS": {
        "speller": "(path TEXT, name TEXT, added_on TIMESTAMP)"
        },
    "FILE_PATH_BASE": {
        "speller": os.path.join(_PATH, "speller")
        },
    "FILE_NAME_BASE": {
        "speller": "text_file_no_"
        },
    "FILE_NAME_SUFFIX": {
        "speller": ".txt"
        }
    }


class DatabaseConnector(object):
    def __init__(self):
        self._open_connection()
        self.conn.row_factory = sqlite3.Row

    def _open_connection(self):
        self.conn = sqlite3.connect(DATABASE_PATH,
                                    detect_types=sqlite3.PARSE_DECLTYPES|
                                    sqlite3.PARSE_COLNAMES)

    def execute(self, query, values=None):
        cur = self.conn.cursor()
        if values:
            cur.execute(query, values)
        else:
            cur.execute(query)
        return cur.fetchall()

    def executemany(self, query, values):
        cur = self.conn.cursor()
        cur.executemany(query, values)
        return cur.fetchall()

    def _create_table(self, app):
        query = "CREATE TABLE IF NOT EXISTS " + CONST_APP["TABLE_NAME"][app] + CONST_APP["TABLE_COLUMNS"][app]
        self.execute(query)

    def _get_table_length(self, app):
        query = "SELECT COUNT(*) FROM " + CONST_APP["TABLE_NAME"][app]
        return self.execute(query)[0][0]

    def add_record(self, app, values):
        self._create_table(app)
        value_placeholders = "(" + ", ".join(["?" for i in range(len(values))]) + ")"
        query = "INSERT INTO " + CONST_APP["TABLE_NAME"][app] + " VALUES " + value_placeholders
        self.execute(query, values)

    def generate_timestamp(self):
        return datetime.now()

    def generate_new_path(self, app):
        self._create_table(app)
        file_no = self._get_table_length(app) + 1
        file_name = CONST_APP["FILE_NAME_BASE"][app] + str(file_no) + CONST_APP["FILE_NAME_SUFFIX"][app]
        return os.path.join(CONST_APP["FILE_PATH_BASE"][app], file_name)

    def get_all_records(self, app):
        self._create_table(app)
        query = "SELECT * FROM " + CONST_APP["TABLE_NAME"][app]
        return self.execute(query)

    def get_n_last_added_records(self, app, n):
        self._create_table(app)
        query = "SELECT * FROM " + CONST_APP["TABLE_NAME"][app] + " ORDER BY added_on DESC LIMIT " + n
        return self.execute(query)

    def commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
