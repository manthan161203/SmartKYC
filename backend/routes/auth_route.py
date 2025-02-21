from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from backend.services.auth_service import AuthService
from backend.schemas.auth_schema import RegisterSchema, LoginSchema
from backend.config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register")
async def register_user(user_data: RegisterSchema, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Call the register_user method from the service
        return await auth_service.register_user(user_data, db)
    except HTTPException as http_exc:
        # Handle HTTP exceptions raised by the service
        raise http_exc
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during registration: {str(e)}"
        )

@router.post("/login")
async def login_user(login_data: LoginSchema, db: Session = Depends(get_db)):
    """Login a user using email or phone number and password."""
    try:
        return await auth_service.login_user(login_data, db)
    except HTTPException as http_exc:
        # Handle HTTP exceptions that are raised by the service
        raise http_exc
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during login: {str(e)}"
        )