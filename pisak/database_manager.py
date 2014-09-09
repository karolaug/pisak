import os
import sqlite3
from datetime import datetime


_PATH = os.path.abspath(os.path.split(__file__)[0])

_DATABASE_PATH = os.path.join(_PATH, "pisak_database.db")


class DatabaseConnector(object):
    def __init__(self):
        self._open_connection()
        self.conn.row_factory = sqlite3.Row

    def _open_connection(self):
        self.conn = sqlite3.connect(_DATABASE_PATH,
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

    def get_table_length(self, table):
        query = "SELECT COUNT(*) FROM " + table
        return self.execute(query)[0][0]

    def generate_timestamp(self):
        return datetime.now()

    def get_all_records(self, table):
        query = "SELECT * FROM " + table
        return self.execute(query)

    def commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
