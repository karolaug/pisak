import time
import sqlite3

DATABASE = "brain_flippers/scores.db"

def _get_db_connection():
    return sqlite3.connect(DATABASE)

def _clean_up(conn):
    conn.commit()
    conn.close()

def _get_today_date():
    return time.strftime("%Y-%m-%d")

def add_record(game, name, score):
    conn = _get_db_connection()
    cur = conn.cursor()
    today = _get_today_date()
    values = (today, name, score)
    query = "INSERT INTO " + game + " VALUES (?, ?, ?)"
    cur.execute(query, values)
    _clean_up(conn)

def get_best_today(game):
    conn = _get_db_connection()
    cur = conn.cursor()
    today = _get_today_date()
    query = "SELECT name, score FROM " + game + " WHERE date=? ORDER BY score DESC LIMIT 10"
    cur.execute(query, (today,))
    records = cur.fetchall()
    _clean_up(conn)
    return records

def get_best_ever(game):
    conn = _get_db_connection()
    cur = conn.cursor()
    query = "SELECT name, score FROM " + game + " ORDER BY score DESC LIMIT 10"
    cur.execute(query)
    records = cur.fetchall()
    _clean_up(conn)
    return records
