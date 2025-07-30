import os, sqlite3
from datetime import datetime

DB_PATH = "/app/data/project_context.db"
os.makedirs("/app/data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS threads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT,
        timestamp TEXT,
        user_input TEXT,
        model_response TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def create_project(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO projects (name, created_at) VALUES (?, ?)", (name, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def list_projects():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM projects")
    rows = [r[0] for r in cursor.fetchall()]
    conn.close()
    return rows

def save_thread(project, user_input, model_response):
    create_project(project)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO threads (project, timestamp, user_input, model_response) VALUES (?, ?, ?, ?)",
                   (project, datetime.now().isoformat(), user_input, model_response))
    conn.commit()
    conn.close()

def get_project_context(project, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_input, model_response FROM threads WHERE project=? ORDER BY id DESC LIMIT ?", (project, limit))
    rows = cursor.fetchall()
    conn.close()
    return "\n".join([f"Q: {q}\nA: {a[:300]}..." for q, a in reversed(rows)])
