from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.schemas.otp_schema import VerifyOTPSchema
from backend.services.auth_service import AuthService
from backend.schemas.auth_schema import RegisterSchema, ChangePasswordSchema
from backend.config.database import get_db
from backend.utils.jwt_middleware import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register")
async def register_user(user_data: RegisterSchema, db: Session = Depends(get_db)):
    return await auth_service.register_user(user_data, db)

@router.post("/login", summary="Login with OAuth2 Password Flow")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return await AuthService.login_user(form_data, db)

@router.post("/verify-otp")
async def verify_otp(otp_data: VerifyOTPSchema, db: Session = Depends(get_db)):
    return await auth_service.verify_otp(otp_data, db)

@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordSchema,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await auth_service.change_password(password_data, current_user, db)
