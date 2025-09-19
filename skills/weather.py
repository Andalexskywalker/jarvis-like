# skills/weather.py
import requests

GEOCODE = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST = "https://api.open-meteo.com/v1/forecast"

def _geocode(city: str):
    r = requests.get(GEOCODE, params={"name": city, "count": 1, "language": "en"})
    if r.status_code != 200: return None
    data = r.json()
    if not data.get("results"): return None
    res = data["results"][0]
    return {
        "name": res["name"],
        "country": res.get("country_code") or res.get("country"),
        "lat": res["latitude"],
        "lon": res["longitude"],
        "tz": res.get("timezone", "auto"),
    }

def _fetch_weather(lat, lon, tz="auto"):
    params = {
        "latitude": lat, "longitude": lon, "timezone": tz,
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    }
    r = requests.get(FORECAST, params=params)
    if r.status_code != 200: return None
    return r.json()

def handle_weather(entities):
    city = (entities.get("city") or "").strip()
    if not city:
        return "Weather where? Try: weather in Lisbon"
    loc = _geocode(city)
    if not loc:
        return f"Couldn't find '{city}'. Try another city."
    wx = _fetch_weather(loc["lat"], loc["lon"], loc["tz"])
    if not wx or "current_weather" not in wx:
        return "Weather service unavailable right now."
    cur = wx["current_weather"]
    daily = wx.get("daily", {})
    tmax = daily.get("temperature_2m_max", ["?"])[0]
    tmin = daily.get("temperature_2m_min", ["?"])[0]
    rain = daily.get("precipitation_sum", ["?"])[0]
    name = f"{loc['name']}, {loc['country']}" if loc.get("country") else loc["name"]
    return (f"{name} — now {cur['temperature']}°C, wind {cur['windspeed']} km/h.\n"
            f"Today: min {tmin}°C / max {tmax}°C, precip {rain} mm.")
