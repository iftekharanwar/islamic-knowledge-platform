from fastapi import APIRouter, HTTPException
from typing import Dict

router = APIRouter(
    prefix="/api/preferences",
    tags=["preferences"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_user_preferences():
    """
    Get user preferences including language and school of thought
    """
    return {"message": "User preferences endpoint"}

@router.post("/")
async def update_user_preferences(preferences: Dict):
    """
    Update user preferences
    """
    return {"message": "Update preferences endpoint"}
