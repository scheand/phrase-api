import os
import datetime
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
import google.generativeai as genai
from cachetools import TTLCache
from .models import PhraseResponse
from utils.config_loader import load_prompts

router = APIRouter()
cache = TTLCache(maxsize=100, ttl=5) # Cache for 5 seconds
# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY:", GEMINI_API_KEY) 
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate a phrase using Gemini
def generate_phrase(theme: str = "motivational") -> str:
    try:
        logging.info(f"generate phrase for theme {theme}")
        response = model.generate_content(
            get_prompt(theme))
        return response.text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating phrase: {str(e)}")
    
def get_prompt(theme: str) -> str:
    return load_prompts()["phrase-prompt"].format(theme=theme)


# Get daily phrase (default: motivational)
@router.get("/phrase", response_model=PhraseResponse)
async def get_daily_phrase():
    today = datetime.date.today().isoformat()
    
    cache_key = f"phrase_{today}_motivational"
    
    if cache_key in cache:
        logging.info(f"Getting phrase from cache for key: {cache_key}")
        phrase = cache[cache_key]
    else:
        phrase = generate_phrase()
        cache[cache_key] = phrase
    
    return PhraseResponse(phrase=phrase, theme="motivational", date=today)

# Get themed phrase
@router.get("/phrase/{theme}", response_model=PhraseResponse)
async def get_themed_phrase(theme: str):
    today = datetime.datetime.now().isoformat()
    return PhraseResponse(phrase=generate_phrase(theme),
                          theme=theme, 
                          date=today)