# nlu.py
import re
from skills import todo, timer

def parse_intent(text):
    t = text.lower().strip()
    # todo add
    m = re.match(r"(?:add|put|remember|todo) (.+)", t)
    if m:
        return {"intent": "todo.add", "entities": {"text": m.group(1), "raw_text": text}}
    # todo show
    if any(k in t for k in ["show todos", "list todos", "my todos", "what are my todos", "show todo"]):
        return {"intent": "todo.show", "entities": {}}
    # timer (minutes)
    m = re.match(r"(?:set|create) (?:a )?timer(?: for)? (\d+)\s*(?:m|min|minutes?)", t)
    if m:
        return {"intent": "timer.set_minutes", "entities": {"minutes": int(m.group(1)), "raw_text": text}}
    # timer seconds
    m = re.match(r"(?:set )?timer (\d+)\s*s", t)
    if m:
        return {"intent": "timer.set_seconds", "entities": {"seconds": int(m.group(1))}}
    # fallback smalltalk
    if t in ("hi","hello","hey"):
        return {"intent":"smalltalk.greet", "entities":{}}
    return {"intent":"fallback", "entities": {"raw_text": text}}
