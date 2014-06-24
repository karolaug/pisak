import time
import sqlite3

DATABASE = "brain_flippers/scores.db"

def _get_today_date():
    return time.strftime("%Y-%m-%d")

def _query_db(query, values=None):
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
    query = "CREATE TABLE " + game + " IF NOT EXISTS"
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
