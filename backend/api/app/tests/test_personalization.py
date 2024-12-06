"""Test personalization features."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
import uuid

@pytest.mark.asyncio
async def test_set_user_preferences(client):
    """Test setting user preferences."""
    preferences = {
        "id": str(uuid.uuid4()),
        "madhab": "hanafi",
        "language": "en",
        "difficulty_level": "beginner",
        "topics_of_interest": ["fiqh", "aqeedah"],
        "learning_path": "basics"
    }
    response = client.post(f"{settings.API_V1_PREFIX}/personalization/preferences", json=preferences)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data

def test_get_learning_paths(client):
    """Test retrieving learning paths."""
    response = client.get(f"{settings.API_V1_PREFIX}/personalization/learning-paths")
    assert response.status_code == 200
    data = response.json()
    assert "paths" in data
    paths = data["paths"]
    assert len(paths) == 3
    assert all(path["id"] in ["basics", "intermediate", "advanced"] for path in paths)

@pytest.mark.asyncio
async def test_ai_response_with_madhab_preference(client, test_supabase):
    """Test AI response considering madhab preference."""
    # Set user preferences first
    preferences = {
        "id": str(uuid.uuid4()),
        "madhab": "hanafi",
        "language": "en",
        "difficulty_level": "beginner"
    }
    response = client.post(f"{settings.API_V1_PREFIX}/personalization/preferences", json=preferences)
    assert response.status_code == 200

    # Test knowledge base response
    query = {
        "query": "What is the ruling on wiping over socks in wudu?",
        "preferences": preferences
    }
    response = client.post(f"{settings.API_V1_PREFIX}/knowledge/search", json=query)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data.get("confidence", 0) > 0
    # Response should mention it's according to Hanafi school
    assert "hanafi" in data["answer"].lower()
