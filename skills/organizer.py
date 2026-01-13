
# skills/organizer.py
import os
import shutil
from pathlib import Path

def get_desktop_path():
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive', 'Ambiente de Trabalho') 
    # Adjusted for your specific path structure since I saw "OneDrive\Ambiente de Trabalho" earlier.
    # A generic one would be os.path.expanduser("~/Desktop") but your setup is specific.

def organize_desktop(args=None):
    """
    Moves files from Desktop into categorized folders (Images, Docs, Installers).
    """
    desktop = Path(get_desktop_path())
    if not desktop.exists():
        return f"Error: Desktop path not found at {desktop}"
    
    # Categories
    folders = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".md"],
        "Installers": [".exe", ".msi", ".bat", ".iso"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"]
    }
    
    stats = {k: 0 for k in folders.keys()}
    
    # Create folders
    for folder in folders:
        (desktop / folder).mkdir(exist_ok=True)
        
    # Move files
    files_moved = 0
    for file in desktop.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            for folder, extensions in folders.items():
                if ext in extensions and file.name != "desktop.ini":
                    try:
                        shutil.move(str(file), str(desktop / folder / file.name))
                        stats[folder] += 1
                        files_moved += 1
                        break
                    except Exception as e:
                        print(f"Failed to move {file.name}: {e}")
                        
    if files_moved == 0:
        return "Desktop is already clean! ✨"
        
    summary = ", ".join([f"{v} {k}" for k,v in stats.items() if v > 0])
    return f"Organized {files_moved} files: {summary}"

def find_file(query):
    """
    Finds a file in the user's home directory (limit depth 2 for speed).
    """
    if isinstance(query, dict): query = query.get('name', '')
    
    root = os.environ['USERPROFILE']
    matches = []
    
    # Simple walk
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip heavy folders
        if "AppData" in dirpath or ".git" in dirpath:
            continue
            
        for f in filenames:
            if query.lower() in f.lower():
                matches.append(os.path.join(dirpath, f))
                if len(matches) >= 3: break
        
        count += 1
        if count > 2000: break # Safety break
        if len(matches) >= 3: break
        
    if not matches:
        return f"No files found matching '{query}'."
        
    return "Found:\n" + "\n".join(matches)
