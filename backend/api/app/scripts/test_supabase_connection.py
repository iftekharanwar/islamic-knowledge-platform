"""Test Supabase connection and capabilities."""
import os
import sys
import asyncio
from pathlib import Path

# Add the parent directory to Python path
current_dir = Path(__file__).resolve().parent
api_dir = current_dir.parent.parent
sys.path.append(str(api_dir))

from app.services.supabase_client import supabase

async def test_connection():
    """Test basic Supabase operations."""
    try:
        # Test table listing
        print("Testing table listing...")
        response = supabase.client.table('islamic_content').select("*").limit(1).execute()
        print(f"Table listing response: {response}")

        # Test raw SQL query
        print("\nTesting raw SQL query...")
        try:
            response = supabase.client.postgrest.query("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                madhab TEXT,
                language TEXT NOT NULL DEFAULT 'en',
                difficulty_level TEXT NOT NULL DEFAULT 'beginner',
                topics_of_interest TEXT[] DEFAULT ARRAY[]::TEXT[],
                learning_path TEXT,
                created_at TIMESTAMPTZ DEFAULT now(),
                updated_at TIMESTAMPTZ DEFAULT now()
            );
            """).execute()
            print(f"Table creation response: {response}")
        except Exception as e:
            print(f"Table creation error: {str(e)}")
            print("Trying alternative method...")
            try:
                # Try using table() method
                response = supabase.client.table('user_preferences').select("*").limit(1).execute()
                print("Table already exists, got response:", response)
            except Exception as table_e:
                print(f"Alternative method error: {str(table_e)}")

    except Exception as e:
        print(f"Connection test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_connection())
