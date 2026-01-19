# skills/clipboard.py
import tkinter as tk

def get_clipboard(_entities=None):
    """
    Reads the current text from the Windows clipboard.
    """
    try:
        root = tk.Tk()
        root.withdraw()
        text = root.clipboard_get()
        root.destroy()
        return text if text else "Clipboard is empty."
    except Exception as e:
        return f"Could not read clipboard: {e}"

def set_clipboard(text: str):
    """
    Copies text to the Windows clipboard.
    """
    try:
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update() # Required to finalize clipboard on some systems
        root.destroy()
        return "Text copied to clipboard."
    except Exception as e:
        return f"Could not write to clipboard: {e}"
