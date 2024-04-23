from fastapi import APIRouter, HTTPException, Query
from ..models.practitioner import Practitioner

router = APIRouter()


@router.get("/practitioner", response_model=Practitioner, responses={400: {"description": "Invalid member ID value"}})
def get_practitioner(memberId: str = Query(..., description="Member ID to be considered for filter")):
    # Dummy data for demonstration
    if memberId != "valid":
        raise HTTPException(status_code=400, detail="Invalid member ID value")
    return Practitioner(
        memberId="123456789",
        fullName="José García García",
        membershipProvince="Madrid",
        medicalSpecialty="Médico especialista en Pediatría",
        membershipState="ALTA",
        workAddress="Calle Singular Nº 0"
    )
