import time
import sqlite3

DATABASE = "brain_flippers/scores.db"

def get_db_connection():
    return sqlite3.connect(DATABASE)

def get_today_date():
    return time.strftime("%Y-%m-%d")

def add_record(game, name, score):
    today = get_today_date()
    values = (today, name, score)
    conn = get_db_connection()
    cur = conn.cursor()
    if game == "monkey":
        cur.execute("""CREATE TABLE IF NOT EXISTS monkey
                    (date TEXT, name TEXT, points REAL)""")
        cur.execute("INSERT INTO monkey VALUES (?, ?, ?)", values)
    clean_up(conn)

def clean_up(conn):
    conn.commit()
    conn.close()
