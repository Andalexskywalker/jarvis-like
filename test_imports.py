
print("Testing imports...")
import datetime
print(f"datetime module: {datetime}")
try:
    print(f"datetime.datetime: {datetime.datetime}")
except AttributeError as e:
    print(f"Error access datetime.datetime: {e}")

from skills import timer, todo, launcher, organizer, creator, voice, system, weather, calc, clock
print("Skills loaded.")
