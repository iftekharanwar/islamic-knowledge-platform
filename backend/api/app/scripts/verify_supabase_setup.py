"""Script to verify Supabase setup and create necessary tables."""
import asyncio
import httpx
from typing import Optional, Dict, Any

class SupabaseVerifier:
    def __init__(self):
        self.url = "https://lewsapkmumthxkspsemo.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxld3NhcGttdW10aHhrc3BzZW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMzNzMyNTIsImV4cCI6MjA0ODk0OTI1Mn0.tnYFIgUGwFi4hLGsQrWeeZkSeX6uKWKh5eU8VZT13NQ"
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    async def check_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.url}/rest/v1/{table_name}?select=count=exact",
                    headers=self.headers
                )
                return response.status_code != 404
        except Exception as e:
            print(f"Error checking table {table_name}: {str(e)}")
            return False

    async def create_user_preferences_table(self) -> bool:
        """Create the user_preferences table if it doesn't exist."""
        try:
            # First check if table exists
            if await self.check_table_exists('user_preferences'):
                print("user_preferences table already exists")
                return True

            # Create table using REST API
            create_table_sql = """
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
            CREATE INDEX IF NOT EXISTS idx_user_preferences_madhab ON user_preferences(madhab);
            CREATE INDEX IF NOT EXISTS idx_user_preferences_learning_path ON user_preferences(learning_path);
            """

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.url}/rest/v1/rpc/exec_sql",
                    headers=self.headers,
                    json={"query": create_table_sql}
                )

                if response.status_code in [200, 201]:
                    print("Successfully created user_preferences table")
                    return True
                else:
                    print(f"Failed to create table. Status: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False

        except Exception as e:
            print(f"Error creating user_preferences table: {str(e)}")
            return False

    async def verify_setup(self) -> None:
        """Verify the entire setup."""
        print("Starting Supabase setup verification...")

        # Check islamic_content table
        if await self.check_table_exists('islamic_content'):
            print("✓ islamic_content table exists")
        else:
            print("✗ islamic_content table missing")

        # Create user_preferences table
        if await self.create_user_preferences_table():
            print("✓ user_preferences table ready")
        else:
            print("✗ Failed to setup user_preferences table")

async def main():
    verifier = SupabaseVerifier()
    await verifier.verify_setup()

if __name__ == "__main__":
    asyncio.run(main())
