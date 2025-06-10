from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import logging
from phrasegen.routes import router as prasegen_router

logging.basicConfig(level=logging.INFO, # Set the minimum level to log
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastAPI app
app = FastAPI(title="Phrase of the Day API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include feature routers
app.include_router(prasegen_router, prefix="/phrase", tags=["phrase"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Phrase of the Day API. Try /phrase or /phrase/{theme}"}
