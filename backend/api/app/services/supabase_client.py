from supabase import create_client, Client
import os
from dotenv import load_dotenv
import json
from typing import Dict, Any, Optional, List
import uuid
import pathlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.url = "https://lewsapkmumthxkspsemo.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxld3NhcGttdW10aHhrc3BzZW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMzNzMyNTIsImV4cCI6MjA0ODk0OTI1Mn0.tnYFIgUGwFi4hLGsQrWeeZkSeX6uKWKh5eU8VZT13NQ"
        self.client: Client = create_client(self.url, self.key)

    async def create_table(self, table_name: str) -> bool:
        """Create a table using simple table operations."""
        try:
            # Try to insert a dummy record to check if table exists
            try:
                self.client.table(table_name).select("*").limit(1).execute()
                logger.info(f"Table {table_name} already exists")
                return True
            except Exception as e:
                if "relation" not in str(e) and "does not exist" not in str(e):
                    logger.error(f"Unexpected error checking table: {e}")
                    return False

            # Table doesn't exist, create it with a simple structure
            if table_name == 'regional_rulings':
                # Create table with minimal structure first
                data = {
                    "id": str(uuid.uuid4()),
                    "region": "test",
                    "topic": "test",
                    "ruling": "test",
                    "context": "test",
                    "scholars": [],
                    "ref_list": [],  # Updated from references to ref_list
                    "cultural_notes": None,
                    "local_practices": None,
                    "created_at": "now()",
                    "updated_at": "now()"
                }

                # Try to insert, which will create the table with appropriate columns
                self.client.table(table_name).insert(data).execute()

                # Clean up test data
                self.client.table(table_name).delete().eq("topic", "test").execute()

                logger.info(f"Successfully created table {table_name}")
                return True

            return False
        except Exception as e:
            logger.error(f"Error creating table {table_name}: {str(e)}")
            return False

    async def get_content(self, table_name: str = 'islamic_content', query: Optional[Dict[str, Any]] = None) -> list:
        try:
            data = self.client.table(table_name).select("*")
            if query:
                for key, value in query.items():
                    data = data.eq(key, value)
            result = data.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting content: {e}")
            return []

    async def insert_content(self, table_name: str, data: Dict[str, Any]) -> Optional[Dict]:
        try:
            await self.create_table(table_name)

            serialized_data = {}
            for k, v in data.items():
                if hasattr(v, 'value'):
                    serialized_data[k] = v.value
                elif isinstance(v, list):
                    serialized_data[k] = v
                else:
                    serialized_data[k] = v

            response = self.client.table(table_name).insert(serialized_data).execute()
            if not response.data:
                print(f"No data returned from insert operation: {response}")
                return None
            return response.data[0]
        except Exception as e:
            print(f"Error inserting content: {e}")
            print(f"Data that failed to insert: {data}")
            return None

    async def search_content(self, search_term: str, table_name: str = 'islamic_content', madhab: Optional[str] = None) -> list:
        try:
            query = self.client.table(table_name)\
                .select("*")\
                .filter("content", "ilike", f"%{search_term}%")

            if madhab:
                query = query.or_(
                    f"content.ilike.%{madhab}%,content.ilike.%general%"
                )

            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error searching content: {e}")
            return []

    async def get_user_preferences(self, user_id: str) -> Optional[Dict]:
        try:
            result = self.client.table('user_preferences')\
                .select("*")\
                .eq('id', user_id)\
                .execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user preferences: {e}")
            return None

    async def set_user_preferences(self, preferences: Dict[str, Any]) -> Optional[Dict]:
        try:
            if 'id' not in preferences:
                preferences['id'] = str(uuid.uuid4())

            await self.create_table('user_preferences')

            response = self.client.table('user_preferences')\
                .upsert(preferences, on_conflict='id')\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error setting user preferences: {e}")
            return None

    async def get_content_by_madhab(self, madhab: str, topic: Optional[str] = None) -> List[Dict]:
        try:
            query = self.client.table('islamic_content')\
                .select("*")\
                .ilike('content', f'%{madhab}%')

            if topic:
                query = query.eq('topic', topic)

            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting madhab content: {e}")
            return []

    async def delete_content(self, table_name: str, query: Optional[Dict[str, Any]] = None) -> bool:
        try:
            delete_query = self.client.table(table_name).delete()
            if query:
                for key, value in query.items():
                    if isinstance(value, dict):
                        for op, val in value.items():
                            if op == '$like':
                                delete_query = delete_query.like(key, val)
                    else:
                        delete_query = delete_query.eq(key, value)

            result = delete_query.execute()
            return True
        except Exception as e:
            print(f"Error deleting content from {table_name}: {e}")
            return False

supabase = SupabaseClient()
