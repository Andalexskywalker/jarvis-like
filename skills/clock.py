# skills/clock.py
from datetime import datetime

def handle_time(_entities=None):
    return "Time now: " + datetime.now().strftime("%H:%M:%S")

def handle_date(_entities=None):
    return "Today is: " + datetime.now().strftime("%Y-%m-%d")
