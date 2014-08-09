from datetime import datetime, date
import sqlite3
from os import getenv
import os.path


home = getenv('HOME')
DATABASE = os.path.join(home, 'pisak_scores.db')
COLUMNS = "(datetime TIMESTAMP, date DATE, name TEXT, score REAL)"


def add_record(game, name, score):
    db = DBConnector()
    db.create_table(game)
    today = _get_today_date()
    now = _get_timestamp()
    values = (now, today, name, score)
    query = "INSERT INTO " + game + " VALUES (?, ?, ?, ?)"
    db.query_db(query, values)
    db.close_connection()

def get_best_today(game):
    db = DBConnector()
    db.create_table(game)
    today = _get_today_date()
    query = "SELECT name, score FROM " + game + " WHERE date=? ORDER BY score DESC, datetime DESC LIMIT 10"
    results = db.query_db(query, (today,))
    db.close_connection()
    return results
    
def get_best_ever(game):
    db = DBConnector()
    db.create_table(game)
    query = "SELECT name, score FROM " + game + " ORDER BY score DESC, datetime DESC LIMIT 10"
    results = db.query_db(query)
    db.close_connection()
    return results

def get_average_today(game):
    db = DBConnector()
    db.create_table(game)
    today = _get_today_date()
    query = "SELECT AVG(score) FROM " + game + " WHERE date=?"
    result = db.query_db(query, (today,))
    db.close_connection()
    if result[0]:
        return result[0][0]

def get_average_ever(game):
    db = DBConnector()
    db.create_table(game)
    query = "SELECT AVG(score) FROM " + game
    result = db.query_db(query)
    db.close_connection()
    if result[0]:
        return result[0][0]

def is_top_ten(game, score):
    top_ten = get_best_today(game)
    if top_ten:
        return score > min(0, *[score for (_name, score) in top_ten])
    else:
        return score > 0


def _get_today_date():
    return date.today()

def _get_timestamp():
    return datetime.now()


class DBConnector(object):
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cur = self.conn.cursor()

    def create_table(self, game):
        query = "CREATE TABLE IF NOT EXISTS " + game + COLUMNS
        self.query_db(query)

    def query_db(self, query, values=None):
        if values:
            self.cur.execute(query, values)
        else:
            self.cur.execute(query)
        return self.cur.fetchall()

    def close_connection(self):
        self.conn.commit()
        self.conn.close()
