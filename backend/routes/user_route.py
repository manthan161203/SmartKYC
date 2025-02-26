from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.user_service import UserService
from backend.schemas.user_schema import UserSchema
from backend.utils.jwt_middleware import get_current_user

router = APIRouter(prefix="/user", tags=["User"])
user_service = UserService()

@router.get("/profile", response_model=UserSchema)
async def get_user_detail(
    current_user: str = Depends(get_current_user),  
    db: Session = Depends(get_db)
):
    user = await UserService.get_user_by_email(current_user, db)
    return user
