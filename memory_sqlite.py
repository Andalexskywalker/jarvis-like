# memory_sqlite.py
import sqlite3
from pathlib import Path

DB_PATH = Path("memory.db")

def _conn():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    return con

# --- Key-Value store (optional, for future preferences) ---
def _ensure_kv(con):
    con.execute("""
    CREATE TABLE IF NOT EXISTS kv (
        k TEXT PRIMARY KEY,
        v TEXT
    )""")

def get(key, default=None):
    con = _conn(); _ensure_kv(con)
    cur = con.execute("SELECT v FROM kv WHERE k=?", (key,))
    row = cur.fetchone()
    con.close()
    return row[0] if row else default

def set_(key, value):
    con = _conn(); _ensure_kv(con)
    con.execute("INSERT INTO kv(k,v) VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=excluded.v", (key, str(value)))
    con.commit(); con.close()

# --- Todos API ---
def add_todo(text: str):
    con = _conn()
    cur = con.execute("INSERT INTO todos(text) VALUES(?)", (text,))
    con.commit()
    tid = cur.lastrowid
    con.close()
    return {"id": tid, "text": text, "done": False}

def list_todos():
    con = _conn()
    rows = con.execute("SELECT id, text, done FROM todos ORDER BY id").fetchall()
    con.close()
    return [{"id": r[0], "text": r[1], "done": bool(r[2])} for r in rows]

def mark_done(todo_id: int):
    con = _conn()
    cur = con.execute("UPDATE todos SET done=1 WHERE id=?", (todo_id,))
    con.commit(); con.close()
    return cur.rowcount > 0

def delete_todo(todo_id: int):
    con = _conn()
    cur = con.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    con.commit(); con.close()
    return cur.rowcount > 0
