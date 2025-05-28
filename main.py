import os
import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from cachetools import TTLCache
import logging

logging.basicConfig(level=logging.INFO, # Set the minimum level to log
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
    return f"""
       Please provide a unique, concise, and motivational quote from a famous person related to the topic of {theme}.
       Include their name and a brief info about him. Ideally, the quote should be connected to a significant event in their life that occurred on today's date."""

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
        logging.info(f"Getting phrase from cache for key: {cache_key}")
        phrase = cache[cache_key]
    else:
        phrase = generate_phrase()
        cache[cache_key] = phrase
    
    return PhraseResponse(phrase=phrase, theme="motivational", date=today)

# Get themed phrase
@app.get("/phrase/{theme}", response_model=PhraseResponse)
async def get_themed_phrase(theme: str):
    today = datetime.datetime.now().isoformat()
    return PhraseResponse(phrase=generate_phrase(theme),
                          theme=theme, 
                          date=today)