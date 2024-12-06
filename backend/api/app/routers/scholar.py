"""Router for handling scholar verification and contributions."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from app.models.scholar import (
    ScholarProfile, ScholarContribution, PeerReview,
    VerificationStatus, Specialization
)
from app.services.supabase_client import supabase
from pydantic import EmailStr

router = APIRouter(
    prefix="/scholars",
    tags=["scholars"],
    responses={404: {"description": "Not found"}}
)

@router.post("/register", response_model=ScholarProfile)
async def register_scholar(
    name: str,
    email: EmailStr,
    credentials: str,
    institution: Optional[str] = None,
    specializations: List[Specialization] = []
):
    """Register a new scholar for verification."""
    try:
        # Check if scholar already exists
        existing = await supabase.get_content(
            table_name='scholar_profiles',
            query={"email": email}
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Scholar with this email already exists"
            )

        scholar_data = {
            "name": name,
            "email": email,
            "credentials": credentials,
            "institution": institution,
            "specializations": [s.value for s in specializations],
            "verification_status": VerificationStatus.PENDING.value,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = await supabase.insert_content(
            table_name='scholar_profiles',
            data=scholar_data
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to register scholar"
            )

        return result[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error registering scholar: {str(e)}"
        )

@router.post("/contributions", response_model=ScholarContribution)
async def submit_contribution(
    scholar_id: str,
    content_id: str,
    contribution_type: str,
    content: str
):
    """Submit a new contribution for peer review."""
    try:
        # Verify scholar exists and is verified
        scholar = await supabase.get_content(
            table_name='scholar_profiles',
            query={"id": scholar_id}
        )
        if not scholar:
            raise HTTPException(
                status_code=404,
                detail="Scholar not found"
            )
        if scholar[0]["verification_status"] != VerificationStatus.VERIFIED.value:
            raise HTTPException(
                status_code=403,
                detail="Only verified scholars can submit contributions"
            )

        contribution_data = {
            "scholar_id": scholar_id,
            "content_id": content_id,
            "contribution_type": contribution_type,
            "content": content,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = await supabase.insert_content(
            table_name='scholar_contributions',
            data=contribution_data
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to submit contribution"
            )

        return result[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error submitting contribution: {str(e)}"
        )

@router.post("/reviews", response_model=PeerReview)
async def submit_review(
    contribution_id: str,
    reviewer_id: str,
    review_type: str,
    comment: str,
    status: str
):
    """Submit a peer review for a contribution."""
    try:
        # Verify reviewer is a verified scholar
        reviewer = await supabase.get_content(
            table_name='scholar_profiles',
            query={"id": reviewer_id}
        )
        if not reviewer or reviewer[0]["verification_status"] != VerificationStatus.VERIFIED.value:
            raise HTTPException(
                status_code=403,
                detail="Only verified scholars can submit reviews"
            )

        # Check if contribution exists
        contribution = await supabase.get_content(
            table_name='scholar_contributions',
            query={"id": contribution_id}
        )
        if not contribution:
            raise HTTPException(
                status_code=404,
                detail="Contribution not found"
            )

        # Check if reviewer has already reviewed this contribution
        existing_review = await supabase.get_content(
            table_name='peer_reviews',
            query={
                "contribution_id": contribution_id,
                "reviewer_id": reviewer_id
            }
        )
        if existing_review:
            raise HTTPException(
                status_code=400,
                detail="You have already reviewed this contribution"
            )

        review_data = {
            "contribution_id": contribution_id,
            "reviewer_id": reviewer_id,
            "review_type": review_type,
            "comment": comment,
            "status": status,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = await supabase.insert_content(
            table_name='peer_reviews',
            data=review_data
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to submit review"
            )

        # Update contribution review count
        await supabase.update_content(
            table_name='scholar_contributions',
            query={"id": contribution_id},
            data={"review_count": contribution[0]["review_count"] + 1}
        )

        return result[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error submitting review: {str(e)}"
        )

@router.get("/contributions/{scholar_id}", response_model=List[ScholarContribution])
async def get_scholar_contributions(scholar_id: str):
    """Get all contributions by a scholar."""
    try:
        contributions = await supabase.get_content(
            table_name='scholar_contributions',
            query={"scholar_id": scholar_id}
        )
        if not contributions:
            raise HTTPException(
                status_code=404,
                detail=f"No contributions found for scholar: {scholar_id}"
            )
        return contributions
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving contributions: {str(e)}"
        )

@router.get("/reviews/{contribution_id}", response_model=List[PeerReview])
async def get_contribution_reviews(contribution_id: str):
    """Get all reviews for a contribution."""
    try:
        reviews = await supabase.get_content(
            table_name='peer_reviews',
            query={"contribution_id": contribution_id}
        )
        if not reviews:
            raise HTTPException(
                status_code=404,
                detail=f"No reviews found for contribution: {contribution_id}"
            )
        return reviews
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving reviews: {str(e)}"
        )
