import sqlite3
import os

def get_db_connection():
    db_path = os.path.abspath("database.db")
    print("Database path:", db_path)

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn