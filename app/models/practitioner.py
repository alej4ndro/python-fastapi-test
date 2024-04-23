from pydantic import BaseModel

class Practitioner(BaseModel):
    memberId: str
    fullName: str
    membershipProvince: str
    medicalSpecialty: str
    membershipState: str
    workAddress: str
