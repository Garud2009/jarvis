import wikipedia, webbrowser # type: ignore

def ask_wiki(q): # wiki lookup
    try:
        return f"Sir, {wikipedia.summary(q, sentences=2)}" # summary res
    except: return "Wiki node failed to find a match, Sir."

def ask_google(q): # google node
    webbrowser.open(f"https://www.google.com/search?q={q}") # launch browser
    return f"Opening search for {q}, Sir."

def launch_site(u): # site node
    u = u if u.startswith('http') else f'https://{u}' # format url
    webbrowser.open(u) # browse
    return f"Launching {u}, Sir."
