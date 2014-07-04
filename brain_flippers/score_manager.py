import time
import sqlite3
from os import getenv
import os.path

home = getenv('HOME')
DATABASE = os.path.join(home, 'scores.db')

def _get_today_date():
    return time.strftime("%Y-%m-%d")

def _query_db(query, values=None):
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.OperationalError:
        f = open(DATABASE, 'w')
        f.close()
        conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    if values:
        cur.execute(query, values)
    else:
        cur.execute(query)
    response = cur.fetchall()
    conn.commit()
    conn.close()
    return response

def _create_table(game):
    query = "CREATE TABLE IF NOT EXISTS " + game + "(date TEXT, name TEXT, score REAL)"
    _query_db(query)
    
def add_record(game, name, score):
    _create_table(game)
    today = _get_today_date()
    values = (today, name, score)
    query = "INSERT INTO " + game + " VALUES (?, ?, ?)"
    _query_db(query, values)

def get_best_today(game):
    _create_table(game)
    today = _get_today_date()
    query = "SELECT name, score FROM " + game + " WHERE date=? ORDER BY score DESC LIMIT 10"
    return _query_db(query, (today,))
    
def get_best_ever(game):
    _create_table(game)
    query = "SELECT name, score FROM " + game + " ORDER BY score DESC LIMIT 10"
    return _query_db(query)

def get_average_today(game):
    _create_table(game)
    today = _get_today_date()
    query = "SELECT AVG(score) FROM " + game + " WHERE date=?"
    response = _query_db(query)
    if response:
        return response[0][0]

def get_average_ever(game):
    _create_table(game)
    query = "SELECT AVG(score) FROM " + game
    response = _query_db(query)
    if response:
        return response[0][0]


def is_top_ten(game, score):
    top_ten = get_best_today(game)
    if top_ten:
        return score > min(0, *[score for (_name, score) in top_ten])
    else:
        return score > 0
