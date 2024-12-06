import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.supabase_client import SupabaseClient
from app.data.regional_sample_data import REGIONAL_RULINGS
import asyncio
import pytest_asyncio

@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)

@pytest.fixture
def test_app():
    """Return the FastAPI application for testing"""
    return app

@pytest_asyncio.fixture(scope="module")
async def test_supabase():
    """Create a test Supabase client."""
    client = SupabaseClient()

    # Setup tables
    try:
        await setup_test_tables(client)
    except Exception as e:
        print(f"Error setting up tables: {e}")

    yield client

    # Cleanup after tests
    await cleanup_test_data(client)

async def setup_test_tables(client):
    """Set up test tables and seed initial data."""
    try:
        # Create regional_rulings table if it doesn't exist
        await client.create_table('regional_rulings')

        # Seed regional rulings data
        for ruling in REGIONAL_RULINGS:
            try:
                await client.insert_content('regional_rulings', ruling)
            except Exception as e:
                print(f"Error seeding ruling: {e}")

    except Exception as e:
        print(f"Error in setup_test_tables: {e}")
        raise e

async def cleanup_test_data(client):
    """Clean up test data after tests."""
    try:
        # Clean up test user preferences
        await client.delete_content('user_preferences', {'id': {'$like': 'test-%'}})

        # Clean up regional rulings
        await client.delete_content('regional_rulings', {})

        print("Test data cleanup completed")
    except Exception as e:
        print(f"Error cleaning up test data: {e}")

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
