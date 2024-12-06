from datetime import datetime
import enum
from typing import Optional, List, Dict, Any
from app.services.supabase_client import supabase

class ContentType(str, enum.Enum):
    QURAN = "quran"
    HADITH = "hadith"
    FATWA = "fatwa"

class Topic(str, enum.Enum):
    AQEEDAH = "aqeedah"
    FIQH = "fiqh"
    TAFSIR = "tafsir"
    SEERAH = "seerah"
    GENERAL = "general"

class Database:
    def __init__(self):
        self.client = supabase

    async def get_content(self, content_type: Optional[ContentType] = None, topic: Optional[Topic] = None) -> List[Dict[str, Any]]:
        query = {}
        if content_type:
            query['content_type'] = content_type
        if topic:
            query['topic'] = topic
        return await self.client.get_content(query=query)

    async def create_content(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.client.insert_content(data)

    async def search_content(self, query: str) -> List[Dict[str, Any]]:
        return await self.client.search_content(query)

db = Database()
