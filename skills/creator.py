# skills/creator.py
import os
from pathlib import Path

def create_text_file(entities):
    """
    Creates a text file with specific content. Args: name (str), content (str)
    """
    name = entities.get("name", "new_file.txt")
    content = entities.get("content", "")
    
    if not name.endswith(".txt"):
        name += ".txt"
        
    # Default to Desktop if no path provided
    desktop = os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'Ambiente de Trabalho')
    path = Path(desktop) / name
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully created {name} on your Desktop."
    except Exception as e:
        return f"Failed to create file: {e}"
