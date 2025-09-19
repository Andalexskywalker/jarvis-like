# skills/timer.py
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# 1) Um único scheduler global em background
_scheduler = BackgroundScheduler()
# start() é idempotente; se já estiver a correr, ignora
_scheduler.start()

def _alarm(message: str):
    # Por agora só imprime. Mais tarde: TTS/notify.
    print("\n⏰ TIMER:", message)

def set_timer_seconds(seconds: int, message: str = "Timer finished"):
    if seconds <= 0:
        return "Timer must be > 0 seconds."
    run_at = datetime.now() + timedelta(seconds=int(seconds))
    _scheduler.add_job(_alarm, 'date', run_date=run_at, args=[message])
    return f"Timer set for {int(seconds)} seconds."

def set_timer_minutes(minutes: int, message: str = "Timer finished"):
    secs = int(minutes) * 60
    return set_timer_seconds(secs, message)
