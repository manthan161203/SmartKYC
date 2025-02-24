from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.services.profile_service import ProfileService
from backend.schemas.profile_schema import GenderTypeResponse
from backend.config.database import get_db

router = APIRouter(prefix="/profile", tags=["Profile"])
profile_service = ProfileService()

@router.get("/gender-types", response_model=List[GenderTypeResponse])
async def get_gender_types(db: Session = Depends(get_db)):
    """Fetch all gender types"""
    return await profile_service.get_gender_types(db)
    