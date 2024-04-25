from fastapi import APIRouter, HTTPException, Query
import httpx
from ..models.practitioner import Practitioner
from ..services.practitioner_service import fetch_practitioner_data

router = APIRouter()


@router.get(
    "/practitioner",
    response_model=Practitioner,
    tags=["practitioner"],
    summary="Finds Practitioner by member ID",
    description="Get practitioner info by member ID",
    responses={
        200: {"description": "Successful operation"},
        400: {"description": "Invalid member ID value"},
        500: {"description": "Internal Server Error"},
    }
)
def get_practitioner(member_id: str = Query(..., description="Member ID to be considered for filter")):
    try:
        practitioner_data = fetch_practitioner_data(member_id)
        if not practitioner_data:
            raise HTTPException(
                status_code=400, detail="Invalid member ID value")
        return practitioner_data
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code,
                            detail=str(exc.response.text))
