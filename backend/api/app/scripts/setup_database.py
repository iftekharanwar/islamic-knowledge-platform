import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.supabase_client import supabase

def setup_database():
    """Set up the database structure and verify it's working."""
    try:
        # Create/verify table structure
        if supabase.create_table():
            print("Database structure created/verified successfully!")
            return True
        else:
            print("Failed to create database structure")
            return False
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database()
