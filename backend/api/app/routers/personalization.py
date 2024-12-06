"""Router for personalization features."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.models.user_preferences import UserPreferences
from app.services.supabase_client import supabase

router = APIRouter(prefix="/personalization", tags=["personalization"])

@router.post("/preferences")
async def set_user_preferences(preferences: UserPreferences):
    """Set user preferences for personalized content."""
    try:
        result = await supabase.set_user_preferences(preferences.model_dump())
        if not result:
            raise HTTPException(status_code=500, detail="Failed to save preferences")
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/learning-paths")
async def get_learning_paths():
    """Get available learning paths."""
    paths = [
        {
            "id": "basics",
            "name": "Islamic Basics",
            "description": "Foundation of Islamic knowledge for beginners",
            "topics": ["Tawheed", "Five Pillars", "Basic Fiqh"]
        },
        {
            "id": "intermediate",
            "name": "Intermediate Studies",
            "description": "Deeper understanding of Islamic principles",
            "topics": ["Detailed Fiqh", "Hadith Studies", "Islamic History"]
        },
        {
            "id": "advanced",
            "name": "Advanced Studies",
            "description": "Advanced topics in Islamic scholarship",
            "topics": ["Usul al-Fiqh", "Comparative Fiqh", "Advanced Hadith"]
        }
    ]
    return {"paths": paths}

@router.get("/preferences/{user_id}")
async def get_user_preferences(user_id: str):
    """Get user preferences."""
    try:
        result = await supabase.get_user_preferences(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Preferences not found")
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
