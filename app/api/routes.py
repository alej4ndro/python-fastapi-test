from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    # Dummy data for demonstration
    return {
        "message": "Service is up"
    }
