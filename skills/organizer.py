
# skills/organizer.py
import os
import shutil
from pathlib import Path

def get_desktop_path():
    """
    Finds the Desktop path dynamically, handling OneDrive and local setups.
    """
    home = Path(os.environ['USERPROFILE'])
    
    # Priority 1: OneDrive Desktop folders (Common in multi-lang setups)
    onedrive_options = [
        home / "OneDrive" / "Desktop",
        home / "OneDrive" / "Ambiente de Trabalho",
        home / "OneDrive" / "Escritorio"
    ]
    
    for p in onedrive_options:
        if p.exists(): return str(p)
        
    # Priority 2: Standard Home Desktop
    local_desktop = home / "Desktop"
    if local_desktop.exists(): return str(local_desktop)
    
    # Fallback: Python's expanduser
    return os.path.expanduser("~/Desktop")

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

def move_file_custom(file_name, target_folder):
    """
    Moves a specific file to a target folder.
    Args:
        file_name (str): Name or path of the file.
        target_folder (str): Name or path of the destination folder.
    """
    desktop = Path(get_desktop_path())
    
    # 1. Resolve Source Path
    source_path = Path(file_name)
    if not source_path.exists():
        # Try looking on Desktop
        source_path = desktop / file_name
        if not source_path.exists():
            return f"Error: Could not find file '{file_name}'."
            
    # 2. Resolve Target Path
    dest_path = Path(target_folder)
    if not dest_path.is_absolute():
        # Assume it's a folder on the Desktop
        dest_path = desktop / target_folder
        
    # Ensure target folder exists
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # 3. Move
    try:
        final_dest = dest_path / source_path.name
        shutil.move(str(source_path), str(final_dest))
        return f"Successfully moved '{source_path.name}' to '{dest_path}'."
    except Exception as e:
        return f"❌ Move failed: {e}"
