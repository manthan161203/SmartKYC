from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.otp_schema import VerifyOTPSchema
from backend.services.auth_service import AuthService
from backend.schemas.auth_schema import RegisterSchema, LoginSchema, ChangePasswordSchema
from backend.config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register")
async def register_user(user_data: RegisterSchema, db: Session = Depends(get_db)):
    """Register a new user"""
    return await auth_service.register_user(user_data, db)

@router.post("/login")
async def login_user(login_data: LoginSchema, db: Session = Depends(get_db)):
    """Login a user using email or phone number and password."""
    return await auth_service.login_user(login_data, db)

@router.post("/change-password")
async def change_password(change_data: ChangePasswordSchema, db: Session = Depends(get_db)):
    """Change a user's password."""
    return await auth_service.change_password(change_data, db)

@router.post("/verify-otp")
async def verify_otp(otp_data: VerifyOTPSchema, db: Session = Depends(get_db)):
    """Verify the OTP entered by the user."""
    return await auth_service.verify_otp(otp_data, db)
