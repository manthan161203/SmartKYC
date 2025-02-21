from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.services.profile_service import ProfileService
from backend.config.database import get_db

router = APIRouter(prefix="/profile", tags=["Profile"])
profile_service = ProfileService()

@router.get("/gender-types")
async def get_gender_types(db: Session = Depends(get_db)):
    """Fetch all gender types"""
    return await profile_service.get_gender_types(db)
