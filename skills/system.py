# skills/system.py
import psutil
import platform

def get_system_stats(args=None):
    """
    Returns CPU, RAM, and Battery stats.
    """
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    
    battery = psutil.sensors_battery()
    bat_str = f", Battery: {battery.percent}%" if battery else ""
    
    uname = platform.uname()
    os_str = f"{uname.system} {uname.release}"
    
    return f"OS: {os_str}, CPU: {cpu}%, RAM: {ram}%{bat_str}"
