from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.services.auth_service import AuthService
from backend.schemas.auth_schema import RegisterSchema
from backend.config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register")
async def register_user(user_data: RegisterSchema, db: Session = Depends(get_db)):
    """Register a new user"""
    return await auth_service.register_user(user_data, db)
