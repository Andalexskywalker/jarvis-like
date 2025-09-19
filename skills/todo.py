
from memory import add_todo, list_todos

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
