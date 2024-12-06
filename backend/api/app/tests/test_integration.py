import pytest
import pytest_asyncio
from app.services.ai_service import AIService
from app.services.supabase_client import supabase

@pytest_asyncio.fixture
async def ai_service():
    service = AIService()
    await service.initialize()
    return service

@pytest.mark.asyncio
async def test_basic_knowledge_retrieval(ai_service):
    """Test basic Islamic knowledge retrieval."""
    queries = [
        "What are the five pillars of Islam?",
        "How do I perform wudu?",
        "What is the importance of Ramadan?"
    ]

    for query in queries:
        response = await ai_service.generate_response(query)
        assert response['confidence'] > 0.5
        assert response['references']
        assert response['verified']

@pytest.mark.asyncio
async def test_madhab_specific_responses(ai_service):
    """Test madhab-specific content adaptation."""
    query = "What is the ruling on wiping over socks?"
    preferences = {
        'madhab': 'hanafi'
    }
    hanafi_response = await ai_service.generate_response(query, preferences=preferences)

    preferences['madhab'] = 'shafii'
    shafii_response = await ai_service.generate_response(query, preferences=preferences)

    assert hanafi_response['answer'] != shafii_response['answer']
    assert all(r['verified'] for r in [hanafi_response, shafii_response])

@pytest.mark.asyncio
async def test_regional_context_integration(ai_service):
    """Test regional context integration."""
    query = "What are the local prayer times?"
    regions = ['middle_east', 'south_asia', 'southeast_asia']

    for region in regions:
        preferences = {'region': region}
        response = await ai_service.generate_response(query, preferences=preferences)
        assert region.lower() in response['answer'].lower()
        assert response['verified']

@pytest.mark.asyncio
async def test_difficulty_level_adaptation(ai_service):
    """Test content adaptation based on learning path."""
    query = "Explain the concept of Tawheed"
    levels = ['basics', 'intermediate', 'advanced']
    responses = []

    for level in levels:
        preferences = {'learning_path': level}
        response = await ai_service.generate_response(query, preferences=preferences)
        responses.append(response['answer'])
        assert response['verified']

    # Verify different complexity levels
    assert len(set(responses)) == len(levels)

@pytest.mark.asyncio
async def test_ethical_compliance_integration(ai_service):
    """Test ethical compliance in integrated responses."""
    sensitive_query = "differences between Islamic schools"
    response = await ai_service.generate_response(sensitive_query)

    assert "sensitive topic" in response['answer'].lower()
    assert response['verified']
    assert all(ref.get('source') for ref in response['references'])

@pytest.mark.asyncio
async def test_offline_content_availability():
    """Test availability of essential content for offline access."""
    essential_topics = ['prayer', 'fasting', 'zakat', 'hajj', 'shahada']

    for topic in essential_topics:
        result = await supabase.get_content('islamic_content', topic)
        assert len(result) > 0
        assert all(content.get('verified', False) for content in result)

@pytest.mark.asyncio
async def test_scholar_verification_system():
    """Test scholar verification and contribution system."""
    # Test scholar profile creation
    scholar_data = {
        'name': 'Test Scholar',
        'credentials': 'Islamic Studies PhD',
        'institution': 'Al-Azhar University',
        'verification_status': 'pending'
    }

    scholar_id = await supabase.create_scholar(scholar_data)
    assert scholar_id

    # Test contribution submission
    contribution = {
        'scholar_id': scholar_id,
        'content_type': 'fatwa',
        'topic': 'prayer',
        'content': 'Test scholarly contribution',
        'references': ['Authentic Source 1'],
        'status': 'pending_review'
    }

    contribution_id = await supabase.create_contribution(contribution)
    assert contribution_id

@pytest.mark.asyncio
async def test_comprehensive_feature_integration(ai_service):
    """Test all features working together."""
    query = "How should I fast in Ramadan while traveling?"
    preferences = {
        'madhab': 'hanafi',
        'region': 'middle_east',
        'learning_path': 'intermediate',
        'language': 'english'
    }

    response = await ai_service.generate_response(query, preferences=preferences)

    # Verify all aspects of the response
    assert response['confidence'] > 0.5
    assert response['verified']
    assert len(response['references']) > 0
    assert preferences['madhab'].lower() in response['answer'].lower()
    assert preferences['region'].lower() in response['answer'].lower()
