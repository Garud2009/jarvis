import os, sys, subprocess, time, threading, random, pyautogui, psutil, screen_brightness_control as sbc # type: ignore
from datetime import datetime
from pathlib import Path
from audio import speak # type: ignore # tts link

def get_time(): return f"Sir, it's {datetime.now().strftime('%I:%M %p')}." # time node

def open_app(n): # os search
    pyautogui.press('win'); time.sleep(0.4) # trigger start
    pyautogui.write(n); time.sleep(0.4) # type query
    pyautogui.press('enter') # launch
    return f'launching {n}'

def vol_up(): [pyautogui.press('volumeup') for _ in range(5)]; return 'volume up' # audio +
def vol_down(): [pyautogui.press('volumedown') for _ in range(5)]; return 'volume down' # audio -
def vol_mute(): pyautogui.press('volumemute'); return 'muted' # audio 0

def get_bright(): # lumen check
    try: return f"Brightness is at {sbc.get_brightness()[0]}%, Sir." # check hardware
    except: return "Lumen sensor failed, Sir." # sensor fail

def set_bright(c): # lumen adjust
    try:
        n = int(''.join(x for x in c if x.isdigit())) # extraction
        sbc.set_brightness(min(max(n, 0), 100)) # voltage control
        return f"Brightness set to {n}%, Sir." # res output
    except: return "Light adjustment failed, Sir." # node fail

def close_it(): # app closer
    try:
        import pygetwindow as gw # type: ignore
        w = gw.getActiveWindow() # check focus
        if w and any(x in w.title.lower() for x in ['code', 'cursor', 'python']):
            return "I won't close your workspace, Sir." # safety guard
    except: pass
    pyautogui.hotkey('ctrl', 'w') # close tab/window
    return 'closed'

def check_pc(): # vitals sensor
    c = psutil.cpu_percent(0.1) # amount of stress I'm under
    m = round(psutil.virtual_memory().available / (1024**3), 1) # ram I haven't eaten yet
    b = psutil.sensors_battery() # energy level
    stat = f"{b.percent}%" if b else "Desktop" # desktop = infinite power
    return f"CPU: {c}%, RAM: {m}GB free, Battery: {stat}, Sir."

def find_file(cmd): # hide and seek
    q = cmd.lower().replace('find', '').replace('file', '').strip()
    if not q: return "Specify the target, Sir. I'm not psychic." # sass
    
    speak(f"Digging through the digital attic for {q}...") # flavor
    roots = [Path.home() / d for d in ["Documents", "Downloads", "Desktop"]] + [Path.home()]
    
    for r in roots: # deep search
        try:
            for p in r.rglob(f"*{q}*"): # match pattern
                if p.is_file():
                    if hasattr(os, 'startfile'):
                        os.startfile(p.parent) # type: ignore # open containing folder
                    return f"Found in {r.name}, Sir."
        except: pass
    return "Not found in common spots, Sir."

def start_timer(c): # timer node
    try:
        n = int(''.join(x for x in c if x.isdigit())) # extraction
        sec = n * 60 if 'min' in str(c) else n # logic
        
        def _beep(): time.sleep(sec); speak("Sir, your timer is up!") # alert
        threading.Thread(target=_beep, daemon=True).start() # background
        return f"Timer set for {n} {'min' if 'min' in str(c) else 'sec'}."
    except: return "Missed the time, Sir."

def play_yt(c): # youtube hook
    try:
        import pywhatkit as kit # type: ignore
        s = c.replace('play', '').replace('youtube', '').strip()
        kit.playonyt(s) # api call
        return f"Playing {s} on YouTube."
    except: return "YouTube node failed, Sir."

def snap_screen(): pyautogui.hotkey('win', 'prtsc'); return 'screenshot saved' # capture

def tell_joke(): # personality matrix
    return random.choice([
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "I would tell you a UDP joke, but you might not get it.",
        "Why did the developer go broke? Because he used up his cache."
    ])

def flip_coin(): return f"It landed on {random.choice(['Heads', 'Tails'])}, Sir." # rng

def lock_pc(): os.system('rundll32.exe user32.dll,LockWorkStation'); return 'locked' # lock sys
def turn_off(): os.system('shutdown /s /t 5'); return 'shutting down' # hard shut
def restart(): os.system('shutdown /r /t 5'); return 'restarting' # reboot
