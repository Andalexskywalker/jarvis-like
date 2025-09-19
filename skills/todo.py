
from memory_sqlite import add_todo, list_todos, mark_done, delete_todo

def handle_todo_add(entities):
    text = entities.get("text") or entities.get("raw_text")
    if not text:
        return "What should I add to your to-do?"
    item = add_todo(text)
    return f"Added todo: [{item['id']}] {item['text']}."

def handle_todo_show(entities):
    todos = list_todos()
    if not todos:
        return "Your to-do list is empty."
    lines = []
    for t in todos:
        status = "✓" if t.get("done") else "·"
        lines.append(f"{t['id']}. {status} {t['text']}")
    return "\n".join(lines)


def handle_todo_done(entities):
    tid = entities.get("id")
    if tid is None:
        return "Which todo id? e.g., done 2"
    ok = mark_done(int(tid))
    return f"Marked todo {tid} as done." if ok else f"Todo {tid} not found."

def handle_todo_delete(entities):
    tid = entities.get("id")
    if tid is None:
        return "Which todo id? e.g., del 2"
    ok = delete_todo(int(tid))
    return f"Deleted todo {tid}." if ok else f"Todo {tid} not found."
