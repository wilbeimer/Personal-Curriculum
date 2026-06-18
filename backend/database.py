import sqlite3


def init_db():
    conn = sqlite3.connect('curriculum.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                color TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect('curriculum.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
