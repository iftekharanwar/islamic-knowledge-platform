"""Models for scholar verification and contributions."""
from typing import List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr

class VerificationStatus(str, Enum):
    """Status of scholar verification."""
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class Specialization(str, Enum):
    """Areas of Islamic scholarship."""
    FIQH = "fiqh"
    HADITH = "hadith"
    TAFSIR = "tafsir"
    AQEEDAH = "aqeedah"
    SEERAH = "seerah"
    GENERAL = "general"

class ScholarProfile(BaseModel):
    """Model for verified Islamic scholars."""
    id: str
    name: str
    email: EmailStr
    credentials: str
    institution: Optional[str] = None
    specializations: List[Specialization]
    verification_status: VerificationStatus
    verification_date: Optional[datetime] = None
    verified_by: Optional[str] = None
    contributions_count: int = 0
    created_at: datetime
    updated_at: datetime

class ScholarContribution(BaseModel):
    """Model for scholar contributions to the knowledge base."""
    id: str
    scholar_id: str
    content_id: str
    contribution_type: str
    content: str
    status: str
    review_count: int = 0
    approved_by: List[str] = []
    rejected_by: List[str] = []
    created_at: datetime
    updated_at: datetime

class PeerReview(BaseModel):
    """Model for peer reviews of scholar contributions."""
    id: str
    contribution_id: str
    reviewer_id: str
    review_type: str
    comment: str
    status: str
    created_at: datetime
    updated_at: datetime
