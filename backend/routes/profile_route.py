from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.services.profile_service import ProfileService
from backend.schemas.profile_schema import GenderTypeResponse
from backend.config.database import get_db
from backend.utils.jwt_middleware import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])
profile_service = ProfileService()

@router.get("/gender-types", response_model=List[GenderTypeResponse])
async def get_gender_types(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Protect route with JWT middleware
):
    """Fetch all gender types"""
    return await profile_service.get_gender_types(db)
    