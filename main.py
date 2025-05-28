import os
import datetime
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from cachetools import TTLCache

# Initialize FastAPI app
app = FastAPI(title="Phrase of the Day API")
cache = TTLCache(maxsize=100, ttl=5) # Cache for 5 seconds


# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY:", GEMINI_API_KEY) 
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Pydantic model for response
class PhraseResponse(BaseModel):
    phrase: str
    theme: str
    date: str
    cache_key: str

# Generate a phrase using Gemini
def generate_phrase(theme: str = "motivational") -> str:
    try:
        response = model.generate_content(
            get_prompt(theme))
        return response.text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating phrase: {str(e)}")
    
def get_prompt(theme: str) -> str:
    return f"""
        Please provide a short phrase or quote for the day related to the topic of [{theme}]. 
        It should include the name of the famous person who said it, along with a brief, defining piece 
        of information about them (e.g., their profession, most famous work, or philosophical school)"""

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Phrase of the Day API. Try /phrase or /phrase/{theme}"}

# Get daily phrase (default: motivational)
@app.get("/phrase", response_model=PhraseResponse)
async def get_daily_phrase():
    today = datetime.date.today().isoformat()
    cache_key = f"phrase_{today}_motivational"
    
    if cache_key in cache:
        phrase = cache[cache_key]
    else:
        phrase = generate_phrase()
        cache[cache_key] = phrase
    
    return PhraseResponse(phrase=phrase, theme="motivational", date=today)

# Get themed phrase
@app.get("/phrase/{theme}", response_model=PhraseResponse)
async def get_themed_phrase(theme: str):
    today = datetime.date.today().isoformat()
    cache_key = f"phrase_{today}_{theme}"
    cache_key_stripped = None    
    if cache_key in cache:
        logging.info(f"Cache hit for key: {cache_key}")        
        phrase = cache[cache_key]
        cache_key_stripped = cache_key
    else:
        phrase = generate_phrase(theme)
        cache[cache_key] = phrase
    
    return PhraseResponse(phrase=phrase, theme=theme, date=today, cache_key=cache_key_stripped)