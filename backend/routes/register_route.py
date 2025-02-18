from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.schemas.user_schema import UserCreate
from backend.service.user_service import register_user, validate_otp_user

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/validate-otp")
def validate_otp_route(email: str, otp: str, db: Session = Depends(get_db)):
    return validate_otp_user(email, otp, db)
