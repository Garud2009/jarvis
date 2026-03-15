import requests # type: ignore

def check_weather(): # atmospheric sensor
    try:
        # node 1: ipapi.co
        g = requests.get('https://ipapi.co/json/', timeout=5).json()
        lat, lon, city = g.get('latitude'), g.get('longitude'), g.get('city')
        
        # node 2: ip-api.com fallback
        if not lat or not lon:
            g = requests.get('http://ip-api.com/json/', timeout=5).json()
            lat, lon, city = g.get('lat'), g.get('lon'), g.get('city')
            
        if not lat or not lon: return "Location node failed, Sir." # blackout
            
        u = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true' # meteo api
        d = requests.get(u, timeout=5).json() # sensor data
        
        if 'current_weather' not in d: return f"Weather station in {city or 'Unknown'} is down, Sir."
            
        w = d['current_weather'] # current node
        return f"Sir, in {city or 'Unknown'}, it's {w.get('temperature')}°C. Winds at {w.get('windspeed')}km/h."
    except: return "Atmospheric sensor error, Sir." # fallback
