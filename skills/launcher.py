# skills/launcher.py
import os, sys, webbrowser
from memory_sqlite import get, set_

# SAFE whitelist — extend as you like
WHITELIST = {
    "youtube": "https://www.youtube.com",
    "github":  "https://github.com",
    "gmail":   "https://mail.google.com",
    "google":  "https://www.google.com",
    "stack":   "https://stackoverflow.com",
    "linkedin":"https://www.linkedin.com",
    # apps are trickier; prefer URLs. Add paths only if you know them.
}

PENDING_KEY = "pending.launch"

def handle_open(entities):
    target = (entities.get("target") or "").lower().strip()
    if not target:
        return "Open what? e.g., open youtube"
    if target not in WHITELIST:
        return f"'{target}' is not in my safe list. Allowed: {', '.join(WHITELIST.keys())}"
    set_(PENDING_KEY, target)
    return f"Open {target}? Reply YES to confirm or NO to cancel."

def _launch(url_or_path):
    # Prefer URLs
    if url_or_path.startswith("http"):
        webbrowser.open(url_or_path)
        return True
    # Basic app open (Windows)
    try:
        if sys.platform.startswith("win"):
            os.startfile(url_or_path)  # type: ignore[attr-defined]
            return True
        elif sys.platform == "darwin":
            os.system(f"open '{url_or_path}'")
            return True
        else:
            os.system(f"xdg-open '{url_or_path}'")
            return True
    except Exception:
        return False

def handle_confirm_yes(_entities=None):
    pending = get(PENDING_KEY)
    if not pending:
        return "Nothing to confirm."
    url = WHITELIST.get(pending)
    ok = _launch(url) if url else False
    set_(PENDING_KEY, None)
    return f"Opening {pending}..." if ok else "Failed to open."

def handle_confirm_no(_entities=None):
    set_(PENDING_KEY, None)
    return "Cancelled."
