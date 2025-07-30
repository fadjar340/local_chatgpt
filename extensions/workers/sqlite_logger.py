import sqlite3
import os

DB_PATH = "/app/data/events.db"

def init_db():
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, type TEXT, details TEXT)")
    conn.commit()
    conn.close()

def log_event(event_type: str, details: str) -> str:
    """
    Logs events into a local SQLite database.
    """
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO logs (type, details) VALUES (?, ?)", (event_type, details))
        conn.commit()
        conn.close()
        return f"🗄️ Event logged [{event_type}]"
    except Exception as e:
        return f"⚠️ Logger Error: {e}"
