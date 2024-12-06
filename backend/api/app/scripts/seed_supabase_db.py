import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.supabase_client import supabase
from app.data.initial_content import initial_content

async def seed_database():
    try:
        table_name = 'islamic_content'
        print(f"Starting to seed {table_name} table...")

        for content in initial_content:
            try:
                result = await supabase.insert_content(
                    table_name,
                    {
                        'content_type': content['content_type'],
                        'topic': content['topic'],
                        'title': content['title'],
                        'content': content['content'],
                        'source': content['source'],
                        'reference': content['reference'],
                        'scholar': content['scholar']
                    }
                )
                print(f"Successfully inserted content: {content['title']}")
            except Exception as e:
                print(f"Error inserting content {content['title']}: {str(e)}")
                continue

        print("Database seeding completed successfully!")

    except Exception as e:
        print(f"Error seeding database: {str(e)}")

if __name__ == "__main__":
    asyncio.run(seed_database())
