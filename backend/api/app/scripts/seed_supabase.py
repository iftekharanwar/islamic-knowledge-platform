import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.supabase_client import supabase
from app.data.initial_content import initial_content

async def seed_supabase():
    try:
        # Create initial content
        for content in initial_content:
            try:
                await supabase.insert_content('islamic_content', content)
                print(f"Successfully inserted content: {content['title']}")
            except Exception as e:
                print(f"Error inserting content '{content['title']}': {e}")
        print("Finished seeding Supabase!")
    except Exception as e:
        print(f"Error seeding Supabase: {e}")

if __name__ == "__main__":
    asyncio.run(seed_supabase())
