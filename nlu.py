import re
from nlu_ml import predict_intent


HELP_PHRASES = ("help", "commands", "what can you do", "how to")

def parse_intent(text):
    t = text.strip()
    tl = t.lower()

    # help
    if any(p in tl for p in HELP_PHRASES):
        return {"intent": "help", "entities": {}}

    # todo add (aliases)
    m = re.match(r"(?:add|todo|remember to|remind me to)\s+(.+)", tl)
    if m:
        return {"intent": "todo.add", "entities": {"text": m.group(1), "raw_text": t}}

    # todo show
    if any(k in tl for k in ["show todos", "list todos", "my todos", "show todo", "todos"]):
        return {"intent": "todo.show", "entities": {}}

    # todo done
    m = re.match(r"(?:done|finish|complete)\s+(\d+)", tl)
    if m:
        return {"intent": "todo.done", "entities": {"id": int(m.group(1))}}

    # todo delete
    m = re.match(r"(?:del|delete|remove)\s+(\d+)", tl)
    if m:
        return {"intent": "todo.delete", "entities": {"id": int(m.group(1))}}

    # timer minutes (e.g., set timer 5m / set a timer for 10 minutes)
    m = re.match(r"(?:set|create)?\s*(?:a )?timer(?: for)?\s*(\d+)\s*(?:m|min|minutes?)", tl)
    if m:
        return {"intent": "timer.set_minutes", "entities": {"minutes": int(m.group(1)), "raw_text": t}}

    # timer seconds (e.g., timer 30s)
    m = re.match(r"(?:set )?timer\s+(\d+)\s*s", tl)
    if m:
        return {"intent": "timer.set_seconds", "entities": {"seconds": int(m.group(1))}}
    # time/date
    if "what time" in tl or "time now" in tl:
        return {"intent": "clock.time", "entities": {}}
    if "what date" in tl or "today date" in tl or "what's the date" in tl:
        return {"intent": "clock.date", "entities": {}}

    # calc
    m = re.match(r"(?:calc|calculate|compute)\s+(.+)", tl)
    if m:
        return {"intent": "calc.eval", "entities": {"expr": m.group(1)}}

    # smalltalk
    if tl in ("hi", "hello", "hey"):
        return {"intent": "smalltalk.greet", "entities": {}}
    
        tl = t.lower()

    # confirmations
    if tl in ("yes","y","sim","ok","okay"):
        return {"intent":"confirm.yes","entities":{}}
    if tl in ("no","n","nao","não","cancel"):
        return {"intent":"confirm.no","entities":{}}

    # weather
    m = re.match(r"(?:weather|forecast)\s+(?:in\s+)?(.+)", tl)
    if m:
        return {"intent":"weather.now","entities":{"city": m.group(1)}}
    m = re.match(r"tempo\s+em\s+(.+)", tl)  # PT
    if m:
        return {"intent":"weather.now","entities":{"city": m.group(1)}}

    # launcher
    m = re.match(r"(?:open|launch)\s+([a-z0-9\-_]+)", tl)
    if m:
        return {"intent":"launch.open","entities":{"target": m.group(1)}}

        # fallback → try ML
    try:
        label, conf = predict_intent(tl)
        if conf >= 0.75:
            return {"intent": label, "entities": {"raw_text": t}}
    except Exception:
        pass
    return {"intent":"fallback","entities":{"raw_text": t}}
