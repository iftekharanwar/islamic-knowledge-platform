"""Script to seed regional rulings data into Supabase."""
from app.services.supabase_client import supabase
from app.data.regional_sample_data import REGIONAL_RULINGS
import asyncio

async def seed_regional_data():
    """Seed regional rulings into the database."""
    try:
        print("Starting to seed regional data...")

        # Insert sample data using table operations
        for ruling in REGIONAL_RULINGS:
            # Convert enum values to strings if needed
            ruling_data = {
                **ruling,
                'region': ruling['region'].value if hasattr(ruling['region'], 'value') else ruling['region']
            }

            result = await supabase.insert_content('regional_rulings', ruling_data)
            if result:
                print(f"Added ruling for {ruling['region']} - {ruling['topic']}")
            else:
                print(f"Failed to add ruling for {ruling['region']} - {ruling['topic']}")

        print("Regional sample data seeding completed")
    except Exception as e:
        print(f"Error seeding regional data: {e}")

if __name__ == "__main__":
    asyncio.run(seed_regional_data())
