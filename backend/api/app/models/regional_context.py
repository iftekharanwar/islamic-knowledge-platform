"""Models for handling regional context in Islamic rulings."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class Region(str, Enum):
    """Supported regions for contextual rulings."""
    MIDDLE_EAST = "middle_east"
    SOUTH_ASIA = "south_asia"
    SOUTHEAST_ASIA = "southeast_asia"
    AFRICA = "africa"
    EUROPE = "europe"
    NORTH_AMERICA = "north_america"
    AUSTRALIA = "australia"

class RegionalRuling(BaseModel):
    """Model for region-specific Islamic rulings."""
    region: Region
    topic: str
    ruling: str
    context: str
    scholars: List[str]
    ref_list: List[str]  # Changed from references to ref_list
    cultural_notes: Optional[str] = None
    local_practices: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
