import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.supabase_client import supabase
from app.data.initial_content import INITIAL_CONTENT

def seed_initial_content():
    """Seed the database with initial Islamic content."""
    try:
        for content in INITIAL_CONTENT:
            print(f"Inserting content: {content['title']}")
            result = supabase.insert_content('islamic_content', content)
            print(f"Successfully inserted: {content['title']}")
        return True
    except Exception as e:
        print(f"Error seeding content: {str(e)}")
        return False

if __name__ == "__main__":
    success = seed_initial_content()
    sys.exit(0 if success else 1)
