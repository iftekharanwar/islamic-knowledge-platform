import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.accessibility import simplify_explanation

client = TestClient(app)

def test_simplify_explanation_beginner():
    """Test that explanations are simplified for beginners"""
    original_text = "The hadith in Sahih al-Bukhari discusses fiqh principles regarding salah."
    simplified = simplify_explanation(original_text, "beginner")

    assert "saying of Prophet Muhammad" in simplified
    assert "Islamic rules" in simplified
    assert "hadith" not in simplified
    assert "fiqh" not in simplified

def test_simplify_explanation_advanced():
    """Test that advanced explanations retain scholarly terms"""
    original_text = "The hadith in Sahih al-Bukhari discusses fiqh principles."
    advanced = simplify_explanation(original_text, "advanced")

    assert "hadith" in advanced
    assert "fiqh" in advanced
    assert advanced == original_text

def test_knowledge_base_with_language(client):
    """Test knowledge base response with language preference"""
    response = client.post(
        "/api/v1/knowledge/search",
        json={
            "query": "What is Salah?",
            "language": "ar",
            "difficultyLevel": "beginner"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert data["confidence"] > 0
    assert len(data["references"]) > 0

def test_knowledge_base_difficulty_levels(client):
    """Test knowledge base responses at different difficulty levels"""
    # Test beginner level
    beginner_response = client.post(
        "/api/v1/knowledge/search",
        json={
            "query": "What is Wudu?",
            "language": "en",
            "difficultyLevel": "beginner"
        }
    )

    # Test advanced level
    advanced_response = client.post(
        "/api/v1/knowledge/search",
        json={
            "query": "What is Wudu?",
            "language": "en",
            "difficultyLevel": "advanced"
        }
    )

    beginner_data = beginner_response.json()
    advanced_data = advanced_response.json()

    assert "ritual ablution" in beginner_data["text"].lower()
    assert len(beginner_data["text"]) <= len(advanced_data["text"])
    assert beginner_response.status_code == 200
    assert advanced_response.status_code == 200
