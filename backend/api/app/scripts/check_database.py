import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.supabase_client import supabase

def check_database_setup():
    """Check if the required database tables exist."""
    try:
        # Try to fetch a single row from the islamic_content table
        result = supabase.get_content('islamic_content', {'limit': 1})
        print("Database tables exist and are accessible")
        return False  # Database is already set up
    except Exception as e:
        if 'relation "islamic_content" does not exist' in str(e):
            print("Database tables need to be created")
            return True  # Database needs to be set up
        print(f"Error checking database: {str(e)}")
        return True  # Assume setup is needed if we can't verify

if __name__ == "__main__":
    needs_setup = check_database_setup()
    print(f"Database setup needed: {needs_setup}")
    sys.exit(0 if not needs_setup else 1)
