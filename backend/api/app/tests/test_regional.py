"""Test regional features."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.models.regional_context import Region
from app.data.regional_sample_data import REGIONAL_RULINGS
import asyncio

@pytest.fixture(scope="module")
async def setup_regional_data():
    """Setup regional test data."""
    from app.services.supabase_client import supabase

    try:
        # Clear existing test data
        await supabase.delete_content('regional_rulings', {"topic": "test_topic"})

        # Insert sample data
        for ruling in REGIONAL_RULINGS:
            await supabase.insert_content('regional_rulings', ruling)
            await asyncio.sleep(0.1)  # Small delay to prevent rate limiting

        yield

        # Cleanup test data
        for ruling in REGIONAL_RULINGS:
            await supabase.delete_content('regional_rulings', {"topic": ruling["topic"]})
    except Exception as e:
        pytest.fail(f"Failed to setup regional data: {str(e)}")

@pytest.mark.asyncio
async def test_get_regions(setup_regional_data):
    """Test retrieving supported regions."""
    client = TestClient(app)
    response = client.get(f"{settings.API_V1_PREFIX}/regional/regions")
    assert response.status_code == 200
    regions = response.json()
    assert len(regions) > 0
    assert all(region in [r.value for r in Region] for region in regions)

@pytest.mark.asyncio
async def test_get_regional_rulings(setup_regional_data):
    """Test retrieving regional rulings."""
    client = TestClient(app)
    region = "southeast_asia"
    response = client.get(f"{settings.API_V1_PREFIX}/regional/rulings/{region}")
    assert response.status_code == 200
    rulings = response.json()
    assert len(rulings) > 0
    assert all(ruling.get("ruling") for ruling in rulings)
    assert all(ruling.get("context") for ruling in rulings)
    assert all(isinstance(ruling.get("ref_list"), list) for ruling in rulings)  # Updated to check ref_list

@pytest.mark.asyncio
async def test_get_regional_topics(setup_regional_data):
    """Test retrieving topics for a region."""
    client = TestClient(app)
    region = "middle_east"
    response = client.get(f"{settings.API_V1_PREFIX}/regional/topics/{region}")
    assert response.status_code == 200
    topics = response.json()
    assert len(topics) > 0
    assert "prayer_times" in topics

@pytest.mark.asyncio
async def test_invalid_region(setup_regional_data):
    """Test handling of invalid region."""
    client = TestClient(app)
    response = client.get(f"{settings.API_V1_PREFIX}/regional/rulings/invalid_region")
    assert response.status_code == 422  # Validation error for invalid enum value

@pytest.mark.asyncio
async def test_search_regional_content(setup_regional_data):
    """Test searching regional content."""
    client = TestClient(app)

    # Test search with just query
    response = client.get(f"{settings.API_V1_PREFIX}/regional/search?query=halal")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert all("halal" in ruling["ruling"].lower() or
              "halal" in ruling["context"].lower() or
              "halal" in ruling.get("cultural_notes", "").lower() or
              "halal" in ruling.get("local_practices", "").lower()
              for ruling in results)

    # Test search with region filter
    response = client.get(
        f"{settings.API_V1_PREFIX}/regional/search?query=prayer&region=middle_east"
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert all(ruling["region"] == "middle_east" for ruling in results)

    # Test search with no results
    response = client.get(
        f"{settings.API_V1_PREFIX}/regional/search?query=nonexistentterm"
    )
    assert response.status_code == 404
    assert "No rulings found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_search_with_topic(setup_regional_data):
    """Test searching regional content with topic filter."""
    client = TestClient(app)
    response = client.get(
        f"{settings.API_V1_PREFIX}/regional/search?query=food&topic=halal_food"
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert all(ruling["topic"] == "halal_food" for ruling in results)

@pytest.mark.asyncio
async def test_cultural_context(setup_regional_data):
    """Test retrieving cultural context."""
    client = TestClient(app)

    # Test getting cultural context for a region
    response = client.get(f"{settings.API_V1_PREFIX}/regional/cultural-context/southeast_asia")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert all(ruling.get("cultural_notes") and ruling.get("local_practices")
              for ruling in results)

    # Test with topic filter
    response = client.get(
        f"{settings.API_V1_PREFIX}/regional/cultural-context/middle_east?topic=prayer_times"
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert all(ruling["topic"] == "prayer_times" for ruling in results)

@pytest.mark.asyncio
async def test_regional_scholars(setup_regional_data):
    """Test retrieving regional scholars."""
    client = TestClient(app)

    # Test getting scholars for a region
    response = client.get(f"{settings.API_V1_PREFIX}/regional/scholars/europe")
    assert response.status_code == 200
    scholars = response.json()
    assert len(scholars) > 0
    assert "European Council for Fatwa and Research" in scholars
