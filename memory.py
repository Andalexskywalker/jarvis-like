# memory.py
import json
from pathlib import Path
from datetime import datetime

DB = Path("memory.json")

def _load():
    if not DB.exists():
        return {}
    return json.loads(DB.read_text(encoding="utf-8"))

def _save(data):
    DB.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def get(key, default=None):
    data = _load()
    return data.get(key, default)

def set_(key, value):
    data = _load()
    data[key] = value
    _save(data)

# simple todo helpers
def add_todo(text):
    data = _load()
    todos = data.get("todos", [])
    todos.append({"id": len(todos)+1, "text": text, "created": datetime.utcnow().isoformat(), "done": False})
    data["todos"] = todos
    _save(data)
    return todos[-1]

def list_todos():
    data = _load()
    return data.get("todos", [])
