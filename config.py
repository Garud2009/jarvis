import os
from dotenv import load_dotenv # type: ignore

load_dotenv() # load .env

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") # auth key
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-lite-preview-02-05:free") # flash node

# frontier free reservoir 2026
OPENROUTER_FALLBACK_MODELS = [
    "nvidia/nemotron-3-super:free", # 120b logic
    "arcee-ai/trinity-large-preview:free", # 400b MoE
    "qwen/qwen3-coder-480b-a35b:free", # 480b coding
    "stepfun/step-3.5-flash:free", # sparse MoE speed
    "google/gemini-2.0-flash:free", # performance
    "google/gemma-3-27b-it:free", # lightweight it
    "openrouter/free" # dynamic auto-router
]

SITE_URL = 'https://github.com/assistant/jarvis'
SITE_NAME = 'Local Python Assistant'
