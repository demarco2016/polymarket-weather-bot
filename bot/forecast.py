import requests
import numpy as np
from datetime import datetime, timedelta

FORECAST_URLS = {
    "ECMWF": "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&models=ecmwf",
    "HRRR": "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&models=hrrr",
    "METAR": "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&models=best_match",
}

CITY_COORDS = {
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6762, 139.6503),
    "Sydney": (-33.8688, 151.2093),
    "Dubai": (25.2048, 55.2708),
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050),
    "Mumbai": (19.0760, 72.8777),
    "Shanghai": (31.2304, 121.4737),
    "São Paulo": (-23.5505, -46.6333),
    "Cairo": (30.0444, 31.2357),
    "Moscow": (55.7558, 37.6173),
    "Toronto": (43.6532, -79.3832),
    "Mexico City": (19.4326, -99.1332),
    "Istanbul": (41.0082, 28.9784),
    "Seoul": (37.5665, 126.9780),
    "Bangkok": (13.7563, 100.5018),
    "Lagos": (6.5244, 3.3792),
    "Buenos Aires": (-34.6037, -58.3816),
    "Jakarta": (-6.2088, 106.8456),
}

def get_forecasts(city):
    lat, lon = CITY_COORDS[city]
    forecasts = {}
    for source, url in FORECAST_URLS.items():
        try:
            resp = requests.get(url.format(lat=lat, lon=lon), timeout=10)
            data = resp.json()
            temps = data["hourly"]["temperature_2m"][:24]
            forecasts[source] = np.mean(temps)
        except Exception as e:
            print(f"  [{source}] error: {e}")
            forecasts[source] = None
    return forecasts

def get_station_data(city):
    lat, lon = CITY_COORDS[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return data["current"]["temperature_2m"]
    except Exception as e:
        print(f"  [station] error: {e}")
        return None
