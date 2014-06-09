import time
import sqlite3

DATABASE = "brain_flippers/scores.db"

def get_db_connection():
    return sqlite3.connect(DATABASE)

def get_today_date():
    return time.strftime("%Y-%m-%d")

def add_record(game, name, score):
    conn = get_db_connection()
    cur = conn.cursor()
    today = get_today_date()
    values = (today, name, score)
    if game == "monkey":
        cur.execute("""CREATE TABLE IF NOT EXISTS monkey
                    (date TEXT, name TEXT, score REAL)""")
        cur.execute("INSERT INTO monkey VALUES (?, ?, ?)", values)
    clean_up(conn)

def get_best_today(game):
    conn = get_db_connection()
    cur = conn.cursor()
    today = get_today_date()
    if game == "monkey":
        cur.execute("SELECT name, score FROM monkey WHERE date=? ORDER BY score DESC LIMIT 10", (today,))
    records = cur.fetchall()
    clean_up(conn)
    return records

def get_best_ever(game):
    conn = get_db_connection()
    cur = conn.cursor()
    if game == "monkey":
        cur.execute("SELECT name, score FROM monkey ORDER BY score DESC LIMIT 10")
    records = cur.fetchall()
    clean_up(conn)
    return records

def clean_up(conn):
    conn.commit()
    conn.close()
