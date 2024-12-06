"""User preferences model for personalization features."""
from typing import Optional
from pydantic import BaseModel

class UserPreferences(BaseModel):
    """User preferences model."""
    id: Optional[str] = None
    madhab: Optional[str] = None  # Islamic school of thought (Hanafi, Shafi'i, etc.)
    language: str = "en"
    difficulty_level: str = "beginner"
    topics_of_interest: list[str] = []  # Topics user wants to focus on
    learning_path: Optional[str] = None  # Current learning path (basics, intermediate, advanced)
