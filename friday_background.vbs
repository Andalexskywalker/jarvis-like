Set WshShell = CreateObject("WScript.Shell")
' Run the main.py script using the virtual environment's pythonw.exe (no console)
' 0 = Hide window, True = Wait for completion
WshShell.Run ".\.venv\Scripts\pythonw.exe main.py --tray", 0, False
