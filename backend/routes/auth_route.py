from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.schemas.otp_schema import VerifyOTPSchema
from backend.services.auth_service import AuthService
from backend.schemas.auth_schema import RegisterSchema, LoginSchema, ChangePasswordSchema, RequestPasswordResetSchema, ResetPasswordSchema
from backend.config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register")
async def register_user(user_data: RegisterSchema, db: Session = Depends(get_db)):
    """Register a new user"""
    return await auth_service.register_user(user_data, db)

@router.post("/login", summary="Login with OAuth2 Password Flow")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),  # Accepts "username" & "password"
    db: Session = Depends(get_db)
):
    """Authenticate user and generate access token."""
    return await AuthService.login_user(form_data, db)

@router.post("/verify-otp")
async def verify_otp(otp_data: VerifyOTPSchema, db: Session = Depends(get_db)):
    """Verify the OTP entered by the user."""
    return await auth_service.verify_otp(otp_data, db)

@router.post("/request-password-reset")
async def request_password_reset(request_data: RequestPasswordResetSchema, db: Session = Depends(get_db)):
    """Request password reset link"""
    return await auth_service.request_password_reset(request_data, db)

@router.post("/reset-password")
async def reset_password(reset_data: ResetPasswordSchema, db: Session = Depends(get_db)):
    """Reset password using the token"""
    return await auth_service.reset_password(reset_data, db)