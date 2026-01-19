# skills/notifications.py
import subprocess

def send_notification(message: str, title: str = "Friday AI"):
    """
    Sends a native Windows toast notification using PowerShell.
    """
    # Escaping single quotes for PowerShell
    msg_escaped = message.replace("'", "''")
    title_escaped = title.replace("'", "''")
    
    ps_command = f"""
    [reflection.assembly]::loadwithpartialname('System.Windows.Forms');
    $notify = New-Object System.Windows.Forms.NotifyIcon;
    $notify.Icon = [System.Drawing.SystemIcons]::Information;
    $notify.Visible = $True;
    $notify.ShowBalloonTip(5000, '{title_escaped}', '{msg_escaped}', [System.Windows.Forms.ToolTipIcon]::Info);
    """
    
    try:
        subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
        return f"Notification sent: {message}"
    except Exception as e:
        return f"Failed to send notification: {e}"
