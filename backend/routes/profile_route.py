from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.services.profile_service import ProfileService
from backend.config.database import get_db

router = APIRouter(prefix="/profile", tags=["Profile"])
profile_service = ProfileService()

@router.get("/gender-types")
async def get_gender_types(db: Session = Depends(get_db)):
    """Fetch all gender types"""
    try:
        return await profile_service.get_gender_types(db)
    except HTTPException as http_exc:
        # Propagate already-raised HTTP exceptions
        raise http_exc
    except Exception as e:
        # Catch any unexpected errors and return a 500 response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
