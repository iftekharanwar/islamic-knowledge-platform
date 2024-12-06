import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.supabase_client import supabase

def verify_database_setup():
    """Verify that the database is properly set up and contains our initial content."""
    try:
        # Check if we can retrieve all content
        print("Checking all content...")
        result = supabase.get_content('islamic_content')
        content = result.data

        if not content:
            print("Error: No content found in database")
            return False

        # Verify we have all content types
        content_types = set(item['content_type'] for item in content)
        expected_types = {'quran', 'hadith', 'fatwa'}
        if not expected_types.issubset(content_types):
            print(f"Error: Missing content types. Found {content_types}, expected {expected_types}")
            return False

        # Verify we have all required topics
        topics = set(item['topic'] for item in content)
        expected_topics = {'aqeedah', 'fiqh'}
        if not expected_topics.issubset(topics):
            print(f"Error: Missing topics. Found {topics}, expected {expected_topics}")
            return False

        # Print verification results
        print("\nDatabase Verification Results:")
        print(f"Total content items: {len(content)}")
        print(f"Content types present: {content_types}")
        print(f"Topics present: {topics}")
        print("\nSample entries:")
        for item in content:
            print(f"\nTitle: {item['title']}")
            print(f"Type: {item['content_type']}")
            print(f"Topic: {item['topic']}")
            print(f"Source: {item['source']}")

        return True
    except Exception as e:
        print(f"Error verifying database: {str(e)}")
        return False

if __name__ == "__main__":
    success = verify_database_setup()
    sys.exit(0 if success else 1)
