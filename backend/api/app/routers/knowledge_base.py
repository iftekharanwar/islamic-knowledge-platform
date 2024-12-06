from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional, Any
from app.models.database import db, ContentType, Topic
from app.services.ai_service import ai_service
from app.routers.accessibility import simplify_explanation
from pydantic import BaseModel
import httpx

router = APIRouter(
    prefix="/knowledge",
    tags=["knowledge"],
    responses={404: {"description": "Not found"}},
)

class SearchRequest(BaseModel):
    query: str
    language: Optional[str] = "en"
    difficultyLevel: Optional[str] = "intermediate"
    school_of_thought: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class SearchResponse(BaseModel):
    text: str
    confidence: float
    references: List[Dict[str, Optional[str]]]
    source_type: Optional[str] = None

@router.post("/search", response_model=SearchResponse)
async def search_knowledge(request: SearchRequest):
    try:
        preferences = {
            'madhab': request.school_of_thought,
            'language': request.language,
            'difficulty_level': request.difficultyLevel
        }

        db_results = await db.search_content(request.query)
        ai_response = await ai_service.generate_response(
            request.query,
            context=db_results,
            preferences=preferences
        )

        answer = ai_response.get("answer", "")
        simplified_answer = simplify_explanation(answer, request.difficultyLevel)

        if request.language != "en":
            try:
                async with httpx.AsyncClient() as client:
                    translation_response = await client.post(
                        "https://libretranslate.com/translate",
                        json={
                            "q": simplified_answer,
                            "source": "en",
                            "target": request.language,
                        }
                    )
                    if translation_response.status_code == 200:
                        data = translation_response.json()
                        simplified_answer = data.get("translatedText", simplified_answer)
            except Exception as e:
                print(f"Translation failed: {e}")

        return SearchResponse(
            text=simplified_answer,
            confidence=ai_response.get("confidence", 0.0),
            references=ai_response.get("references", []),
            source_type=ai_response.get("source_type")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topics")
async def get_topics() -> Dict[str, List[str]]:
    return {"topics": [topic.value for topic in Topic]}

@router.get("/content/{content_type}")
async def get_content_by_type(
    content_type: ContentType,
    topic: Optional[Topic] = None,
) -> List[Dict]:
    try:
        content = await db.get_content(content_type, topic)
        if not content:
            raise HTTPException(status_code=404, detail="No content found")
        return content
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
