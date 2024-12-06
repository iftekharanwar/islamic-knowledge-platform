from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
import httpx
from app.config import settings

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@router.post("/translate")
async def translate_text(request: TranslationRequest):
    """
    Translate text using LibreTranslate API
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://libretranslate.com/translate",
                json={
                    "q": request.text,
                    "source": "en",
                    "target": request.target_language,
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=500, detail="Translation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def simplify_explanation(text: str, level: str) -> str:
    """
    Adjust explanation based on user's knowledge level
    """
    if level == "beginner":
        # Remove complex terminology, add basic explanations
        return text.replace("hadith", "saying of Prophet Muhammad (peace be upon him)").\
                   replace("fiqh", "Islamic rules").\
                   replace("fatwa", "Islamic ruling")
    elif level == "intermediate":
        # Keep some terminology but provide context
        return text
    else:  # advanced
        # Keep original scholarly text
        return text
