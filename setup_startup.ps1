# Create a startup shortcut (No Admin required)
$WshShell = New-Object -ComObject WScript.Shell
$StartupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$ShortcutPath = Join-Path $StartupFolder "FridayAI.lnk"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\andal\OneDrive\Ambiente de Trabalho\projetos\jarvis-like-1\.venv\Scripts\pythonw.exe"
$Shortcut.Arguments = "main.py --tray"
$Shortcut.WorkingDirectory = "C:\Users\andal\OneDrive\Ambiente de Trabalho\projetos\jarvis-like-1"
$Shortcut.Save()

Write-Host "✅ Friday AI has been added to your Startup folder!" -ForegroundColor Green
Write-Host "No Administrator rights were needed. She'll start every time you log in."
