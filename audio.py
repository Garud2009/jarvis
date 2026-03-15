import time, os, uuid, asyncio, pygame, edge_tts # type: ignore # the usual suspects
import speech_recognition as sr # type: ignore # ears of the system

try: import winsound # windows only
except: winsound = None # linux/mac fallback

pygame.mixer.init() # init audio dev

def speak(text): # tts node
    if not text: return # skip empty
    print(f'Jarvis: {text}', flush=True) # force sync print
    f = f'v_{uuid.uuid4().hex}.mp3' # temp file
    try:
        async def _run(): # async pipe
            await edge_tts.Communicate(text, 'en-US-ChristopherNeural', rate='+35%').save(f)
        asyncio.run(_run()) # fire pipe
        
        if not os.path.exists(f): return # check file
        
        pygame.mixer.music.load(f) # stage audio
        pygame.mixer.music.play() # play audio
        while pygame.mixer.music.get_busy(): time.sleep(0.05) # wait for end
        pygame.mixer.music.unload() # release file
        
        for _ in range(15): # windows file-lock cage fight
            try:
                if not os.path.exists(f): break # nothing to do
                os.remove(f) # try delete
                break # success
            except: time.sleep(0.2) # wait for process release
    except Exception as e: # failover
        print(f'Audio Error: {e}', flush=True) # log fail
        if os.path.exists(f): 
            try: os.remove(f) # last ditch
            except: pass

rec = sr.Recognizer() # stt node
rec.pause_threshold = 0.5 # fast switching

def listen(): # mic processor
    with sr.Microphone() as src: # open mic
        if winsound: # audio cue
            try: 
                beep = getattr(winsound, 'Beep', None)
                if beep: beep(1000, 50) # haptic beep
            except: pass
        
        rec.adjust_for_ambient_noise(src, 0.3) # faster filter
        try:
            audio = rec.listen(src, timeout=2, phrase_time_limit=3) # hyper capture
            query = rec.recognize_google(audio) # cloud stt
            print(f'You: {query}') # log query
            return query.lower() # return lower
        except: return "" # silent fail
