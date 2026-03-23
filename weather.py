import requests # type: ignore

_WIND_CODE = { # WMO weather codes - because "1" means nothing to humans
    0:"clear skies", 1:"mainly clear", 2:"partly cloudy", 3:"overcast",
    45:"foggy", 48:"icy fog", 51:"light drizzle", 61:"light rain",
    71:"light snow", 80:"rain showers", 95:"thunderstorm"
}

def check_weather(): # atmospheric sensor
    try:
        lat, lon, city = None, None, None

        # node 1: ip-api.com — free, no key, reliable (tested)
        try:
            g = requests.get('http://ip-api.com/json/', timeout=5).json()
            if g.get('status') == 'success':
                lat, lon, city = g.get('lat'), g.get('lon'), g.get('city')
        except requests.RequestException: pass

        # node 2: ipapi.co — fallback (rate-limited often)
        if not lat or not lon:
            try:
                g = requests.get('https://ipapi.co/json/', timeout=5).json()
                if not g.get('error'): # skip if rate limited
                    lat, lon, city = g.get('latitude'), g.get('longitude'), g.get('city')
            except requests.RequestException: pass

        if not lat or not lon: return "Location node is dead, Sir. Both geo-IP feeds timed out." # blackout

        u = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true' # meteo
        d = requests.get(u, timeout=5).json()

        if 'current_weather' not in d: return f"Weather station for {city or 'your location'} is offline, Sir."

        w = d['current_weather']
        cond = _WIND_CODE.get(w.get('weathercode', -1), "unknown conditions") # human readable
        return f"Sir, {city or 'your area'}: {w.get('temperature')}°C, {cond}. Winds at {w.get('windspeed')} km/h."
    except requests.RequestException as e: return f"Atmospheric sensor error, Sir. ({e})" # specific, not silent
