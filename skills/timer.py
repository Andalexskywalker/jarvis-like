# skills/timer.py
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Event
import time

_scheduler = BackgroundScheduler()
_scheduler.start()

def _alarm(message):
    print("\n⏰ TIMER:", message)  # placeholder - replace with TTS later

def set_timer_seconds(seconds, message="Timer finished"):
    run_at = time.time() + seconds
    _scheduler.add_job(_alarm, 'date', run_date=time.fromtimestamp(run_at), args=[message])
    return f"Timer set for {seconds} seconds."

# convenience wrapper for minutes/hours in NLU
def set_timer_minutes(minutes, message="Timer finished"):
    return set_timer_seconds(int(minutes*60), message)
