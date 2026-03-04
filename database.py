import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "data", "items.db"))


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS items "
        "(id INTEGER PRIMARY KEY, name TEXT NOT NULL, value TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
