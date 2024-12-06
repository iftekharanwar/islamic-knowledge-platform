"""Script to seed madhab-specific content into Supabase."""
import asyncio
from app.services.supabase_client import supabase
from app.data.madhab_specific_content import MADHAB_CONTENT

async def seed_madhab_content():
    """Seed madhab-specific content into the database."""
    try:
        print("Seeding madhab-specific content...")
        for content in MADHAB_CONTENT:
            await supabase.insert_content('islamic_content', content)
        print("Successfully seeded madhab-specific content.")
    except Exception as e:
        print(f"Error seeding madhab-specific content: {str(e)}")

if __name__ == "__main__":
    asyncio.run(seed_madhab_content())
