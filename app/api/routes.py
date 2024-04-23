from fastapi import APIRouter, HTTPException, Query
from typing import Any
from ..services.practitioner_service import fetch_practitioner_data
import httpx

router = APIRouter()


@router.get("/practitioner", response_model=Any, responses={
    400: {"description": "Invalid member ID value"},
})
def get_practitioner(memberId: str = Query(..., description="Member ID to be considered for filter")):
    try:
        practitioner_data = fetch_practitioner_data(memberId)
        if not practitioner_data:
            raise HTTPException(
                status_code=404, detail="Practitioner not found")
        return practitioner_data
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code,
                            detail=str(exc.response.text))
