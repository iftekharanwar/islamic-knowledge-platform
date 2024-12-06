"""Script to seed basic Islamic terms into the database."""

import asyncio
from app.services.supabase_client import supabase
from app.data.basic_islamic_terms import BASIC_TERMS

async def seed_basic_terms():
    """Seed basic Islamic terms into the database."""
    try:
        for term in BASIC_TERMS:
            await supabase.insert_content('islamic_content', term)
        print("Successfully seeded basic Islamic terms")
    except Exception as e:
        print(f"Error seeding basic terms: {e}")

if __name__ == "__main__":
    asyncio.run(seed_basic_terms())
