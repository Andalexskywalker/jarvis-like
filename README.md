# Jarvis-Like 

A tiny, extensible Python assistant (text-first) you can run locally.  
Type natural commands like “add -taskname-”, “show todos”, or “set timer 5m” and it routes to simple “skills”.  
Designed to be easy to read, hack, and grow into your own “cartoon AI”.

##  Features (MVP)
-  **Rule-based NLU**: regex/keywords → intents + entities  
-  **To-Do skill**: add and list tasks (JSON-backed storage)  
-  **Timer skill**: set minute/second timers (APScheduler)  
-  **Simple memory**: tiny JSON “database” (`memory.json`)  
-  **Modular**: drop-in skills folder, easy to add new commands  
-  **Web UI** with Gradio (phone friendly)

##  Project Structure
```
jarvis-like/
├─ main.py            # entry point: routes text → skills (CLI + optional Gradio)
├─ nlu.py             # intent parser (regex keywords → intents/entities)
├─ memory.py          # JSON storage (todos, key-value)
├─ skills/
│   ├─ __init__.py
│   ├─ todo.py        # todo.add / todo.show
│   └─ timer.py       # timer.set_minutes / timer.set_seconds
├─ requirements.txt
└─ README.md
```

##  Quick Start
```bash
# 1) Create and activate a virtual env (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run (CLI mode)
python main.py
```

**Try these commands in the CLI:**
```
add buy milk
show todos
set timer 1m
set timer 30s
```

> A new file will be added in you file, memory.json, where it will add these informations.

## Web UI (Gradio)
This little app uses gradio as UI system, Gradio will open a local URL you can also visit from your phone (same Wi-Fi).  

## Adding a New Skill (example)
1) Create a new file in `skills/` (e.g., `clock.py`) with a simple handler:
```python
# skills/clock.py
from datetime import datetime

def handle_time(_entities=None):
    return "Time now: " + datetime.now().strftime("%H:%M:%S")
```
2) Import and route in **`main.py`**:
```python
from skills import clock
# ...
if intent == "clock.time":
    return clock.handle_time(ent)
```
3) Add a regex in **`nlu.py`** to recognize the command:
```python
if "what time" in t or "time now" in t:
    return {"intent": "clock.time", "entities": {}}
```

##  Roadmap
-  **Speech**: Whisper/Vosk (STT) + pyttsx3/edge-tts (TTS)
-  **Smarter NLU**: scikit-learn classifier for many intents
-  **Better timers**: desktop notifications or TTS alarm
-  **Richer memory**: mark todo done, delete, categories, due dates
-  **FastAPI backend**: clean API for mobile/web clients
-  **Android (Termux/Kivy)** or **PWA** for phone-like experience

##  Tech Notes
- **NLU** is intentionally simple: easy to read and extend, its also my first time making thes kind of understanding systems so it has to be simple.
- **Memory** uses JSON so you don’t need a DB setup; swap to SQLite later if you like.
- **APScheduler** runs timers in-process while the app is running.

##  Contributing
Issues and PRs are welcome! Good first contributions:
- Add a small skill (weather, calculator, launcher)
- Improve NLU patterns or tests
- Polish the Gradio UI (history, buttons)

##  License
MIT — do whatever you want, just keep the notice.

##  Disclaimer
This is a learning/prototyping project. It’s local-first and not hardened for production.  
Add authentication/permissions and safety checks before exposing tools that control your system.

---
