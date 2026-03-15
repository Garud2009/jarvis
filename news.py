import requests, random # type: ignore
from bs4 import BeautifulSoup # type: ignore

def fetch_world_news(): # multi-node news sensor
    feeds = { # intelligence reservoir
        'world': 'https://feeds.bbci.co.uk/news/world/rss.xml',
        'tech': 'https://feeds.bbci.co.uk/news/technology/rss.xml',
        'science': 'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml'
    }
    try:
        cat = random.choice(list(feeds.keys())) # pick a flavor
        r = requests.get(feeds[cat], timeout=10) # fetch node
        s = BeautifulSoup(r.content, 'xml') # parse structure
        items = s.find_all('item')[:3] # top headlines
        
        titles = [i.title.text for i in items] # collect intel
        return f"Sir, the latest {cat} headlines: {'... '.join(titles)}."
    except Exception as e: 
        print(f"News Error: {e}") # internal log
        return "Intelligence feed timed out, Sir." # comms fail
