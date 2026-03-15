import os, sys, time, json, requests # type: ignore
import config # type: ignore

sys.path.append(os.path.dirname(os.path.abspath(__file__))) # env path

sys_prompt = """You are Jarvis, a concise AI assistant. Speak naturally, no markdown. End every response with 'Sir'."""

mem_file = 'memory.json' # brain file
chat_history: list = [] # short term mem

if os.path.exists(mem_file): # load history
    try:
        with open(mem_file, 'r') as f: chat_history = json.load(f)
    except: pass

def save_mem(): # dump brain
    try:
        with open(mem_file, 'w') as f: json.dump(chat_history[-15:], f) # type: ignore
    except: pass

def generate_response(prompt): # neural processor
    if not config.OPENROUTER_API_KEY or 'your_api' in str(config.OPENROUTER_API_KEY):
        return "Sir, your OpenRouter key is missing in the .env."

    global chat_history
    chat_history.append({'role': 'user', 'content': prompt}) # store prompt
    
    if len(chat_history) > 12: # neural pruning
        chat_history = chat_history[:2] + chat_history[-10:] # preserve early context + recent
    
    hdrs = { # api headers
        'Authorization': f'Bearer {config.OPENROUTER_API_KEY}',
        'HTTP-Referer': 'http://localhost:3000',
        'X-Title': 'Jarvis Nexus',
        'Content-Type': 'application/json'
    }

    models = [config.OPENROUTER_MODEL] + [m for m in config.OPENROUTER_FALLBACK_MODELS if m != config.OPENROUTER_MODEL]
    payload = {'role': 'system', 'content': sys_prompt} # system node
    
    for m in models: # trying to find a node that isn't sleeping
        try:
            r = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=hdrs,
                json={'model': m, 'messages': [payload] + chat_history[-8:]}, # type: ignore # context dump
                timeout=20
            )
            if r.status_code != 200: continue # node had a stroke
            
            data = r.json() # grabbing sparks of genius
            out = data['choices'][0]['message']['content'].strip()
            if '</think>' in out: out = out.split('</think>')[-1].strip() # ignore the inner monologue
            
            chat_history.append({'role': 'assistant', 'content': out}) # adding to my infinite wisdom
            save_mem() # don't forget the trauma
            return out # dropping the knowledge
        except: time.sleep(0.5) # contemplating life for 0.5s
            
    return "The neural network is having an existential crisis, Sir." # blackout
