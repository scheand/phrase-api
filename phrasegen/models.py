from pydantic import BaseModel

class PhraseResponse(BaseModel):
    phrase: str
    theme: str
    date: str
