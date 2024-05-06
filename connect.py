import sqlite3
from contextlib import contextmanager

database = './hw1.db'

@contextmanager
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = 1")
    yield conn
    conn.rollback()
    conn.close()

