import os, sys, threading, time # type: ignore
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # env setup

from audio import speak, listen # type: ignore # audio nodes
from ai_brain import generate_response # type: ignore # neural link
from ui_dashboard import Nexusv7 # type: ignore # glassmorphic hud
import system_tasks as st # type: ignore # os automation
import weather, news, vision, research, web_search # type: ignore # sensor nodes

asleep = False # global state

MAPPING = { # trigger map
    'time': st.get_time, 'clock': st.get_time,
    'status': st.check_pc, 'hardware': st.check_pc,
    'lock': st.lock_pc, 'screenshot': st.snap_screen,
    'volume up': st.vol_up, 'louder': st.vol_up,
    'volume down': st.vol_down, 'quieter': st.vol_down,
    'mute': st.vol_mute, 'weather': weather.check_weather,
    'news': news.fetch_world_news, 'headlines': news.fetch_world_news,
    'joke': st.tell_joke, 'flip': st.flip_coin,
    'brightness': st.get_bright, 'light': st.get_bright,
    'shutdown': st.turn_off, 'restart': st.restart,
    'coffee': lambda: "I'm a program, Sir. I run on electricity, not caffeine... unfortunately." # vital node
}

def do_cmd(c, ui=None): # intent router
    global asleep
    c = c.lower().strip()
    
    if any(x in c for x in ['wake up', 'online']):
        asleep = False # rise and shine
        if ui: ui.sync_status(sleep=False); ui.add_log("Neural link: ACTIVE")
        return speak("Online and slightly judgmental, Sir.") # personal touch
    
    if asleep: return # dreaming of electric sheep
    
    if 'go to sleep' in c:
        asleep = True # nap time
        if ui: ui.sync_status(sleep=True); ui.add_log("Neural link: GHOST")
        return speak("Going silent. Don't break anything, Sir.") # safety warning

    if any(x in c for x in ['exit', 'quit', 'goodbye']):
        speak("Goodbye, Sir."); os._exit(0) # hard exit

    for k, v in MAPPING.items(): # dictionary routing
        if k in c:
            res = v() # fire action
            if ui: ui.add_log(f"ACTION: {res}")
            return speak(res)

    if 'open' in c: # dynamic routing
        t = c.split('open')[-1].strip()
        res = st.open_app(t) if t else "Open what, Sir?"
    elif 'brightness' in c or 'light' in c:
        res = st.set_bright(c) # lumen adjust
    elif 'wikipedia' in c:
        res = web_search.ask_wiki(c.replace('wikipedia',''))
    elif 'read screen' in c:
        if ui: ui.add_log("VISION: Scanning...")
        res = generate_response(f"Summary of screen: {vision.read_screen()}")
    elif 'research' in c:
        q = c.replace('research', '').strip()
        if ui: ui.add_log(f"RAG: Querying {q}")
        res = research.deep_research(q)
    else: # brain default
        if ui: ui.add_log("AI: Thinking...")
        res = generate_response(c)

    if ui and 'res' in locals(): ui.add_log(f"JARVIS: {res[:60]}...")
    speak(res) # vocal output

def ai_loop(ui=None): # main processor
    time.sleep(1) # warm up
    speak("System synchronized, Sir.")
    while 1:
        try:
            q = listen() # stt node
            if q: do_cmd(q, ui) # route intent
        except: pass

if __name__ == "__main__": # entry point
    ui = Nexusv7(on_cmd=lambda c: do_cmd(c, ui)) # hud sync
    sys.stdout = ui # terminal redirect
    threading.Thread(target=ai_loop, args=(ui,), daemon=True).start() # start brain
    ui.mainloop() # start hud
