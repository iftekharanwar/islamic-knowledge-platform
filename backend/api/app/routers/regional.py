"""Router for handling region-specific Islamic content and rulings."""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.regional_context import Region, RegionalRuling
from app.services.supabase_client import supabase

router = APIRouter(
    prefix="/regional",
    tags=["regional"],
    responses={404: {"description": "Not found"}}
)

@router.get("/regions", response_model=List[str])
async def get_regions():
    """Get list of supported regions."""
    return [region.value for region in Region]

@router.get("/rulings/{region}", response_model=List[RegionalRuling])
async def get_regional_rulings(
    region: Region,
    topic: Optional[str] = None
):
    """Get rulings specific to a region, optionally filtered by topic."""
    try:
        query = {
            "region": region.value
        }
        if topic:
            query["topic"] = topic

        rulings = await supabase.get_content(
            table_name='regional_rulings',
            query=query
        )

        if not rulings:
            if topic:
                raise HTTPException(
                    status_code=404,
                    detail=f"No rulings found for region '{region}' and topic '{topic}'"
                )
            raise HTTPException(
                status_code=404,
                detail=f"No rulings found for region: {region}"
            )

        # Validate the response format
        for ruling in rulings:
            if not all(key in ruling for key in ["ruling", "context", "ref_list"]):
                raise HTTPException(
                    status_code=500,
                    detail="Invalid ruling format in database"
                )

        return rulings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving regional rulings: {str(e)}"
        )

@router.get("/topics/{region}", response_model=List[str])
async def get_regional_topics(region: Region):
    """Get list of topics with regional rulings."""
    try:
        rulings = await supabase.get_content(
            table_name='regional_rulings',
            query={"region": region.value}
        )

        if not rulings:
            raise HTTPException(
                status_code=404,
                detail=f"No topics found for region: {region}"
            )

        # Extract unique topics from the rulings
        topics = list(set(ruling["topic"] for ruling in rulings))
        topics.sort()  # Sort topics alphabetically
        return topics
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving regional topics: {str(e)}"
        )

@router.get("/search", response_model=List[RegionalRuling])
async def search_regional_content(
    query: str,
    region: Optional[Region] = None,
    topic: Optional[str] = None
):
    """Search regional rulings by content, optionally filtered by region and topic."""
    try:
        # Use full-text search on relevant columns
        search_query = f"%{query}%"  # For LIKE query
        filters = []

        # Build base query
        base_query = {
            "ruling": {"$ilike": search_query},
            "$or": [
                {"context": {"$ilike": search_query}},
                {"cultural_notes": {"$ilike": search_query}},
                {"local_practices": {"$ilike": search_query}}
            ]
        }

        if region:
            filters.append({"region": region.value})
        if topic:
            filters.append({"topic": topic})

        # Combine all filters
        if filters:
            base_query["$and"] = filters

        result = await supabase.get_content(
            table_name='regional_rulings',
            query=base_query
        )

        rulings = result if result else []

        if not rulings:
            filters_text = []
            if region:
                filters_text.append(f"region '{region}'")
            if topic:
                filters_text.append(f"topic '{topic}'")
            filter_text = " and ".join(filters_text)
            detail = f"No rulings found matching '{query}'"
            if filter_text:
                detail += f" for {filter_text}"
            raise HTTPException(
                status_code=404,
                detail=detail
            )

        return rulings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching regional content: {str(e)}"
        )

@router.get("/cultural-context/{region}", response_model=List[RegionalRuling])
async def get_cultural_context(
    region: Region,
    topic: Optional[str] = None
):
    """Get cultural context and local practices for a region."""
    try:
        query = {
            "region": region.value,
            "$and": [
                {"cultural_notes": {"$neq": None}},
                {"local_practices": {"$neq": None}}
            ]
        }

        if topic:
            query["topic"] = topic

        rulings = await supabase.get_content(
            table_name='regional_rulings',
            query=query
        )

        if not rulings:
            detail = f"No cultural context found for region: {region}"
            if topic:
                detail += f" and topic: {topic}"
            raise HTTPException(
                status_code=404,
                detail=detail
            )

        return rulings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving cultural context: {str(e)}"
        )

@router.get("/scholars/{region}", response_model=List[str])
async def get_regional_scholars(region: Region):
    """Get list of scholars associated with a region."""
    try:
        rulings = await supabase.get_content(
            table_name='regional_rulings',
            query={"region": region.value}
        )

        if not rulings:
            raise HTTPException(
                status_code=404,
                detail=f"No scholars found for region: {region}"
            )

        # Extract unique scholars from all rulings
        scholars = list(set(
            scholar
            for ruling in rulings
            for scholar in ruling.get("scholars", [])
        ))
        scholars.sort()  # Sort alphabetically
        return scholars
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving regional scholars: {str(e)}"
        )
