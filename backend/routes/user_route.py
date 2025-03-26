import os
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.user_service import UserService
from backend.schemas.user_schema import UserSchema, EditUserSchema
from backend.utils.jwt_middleware import get_current_user

router = APIRouter(prefix="/user", tags=["User"])
user_service = UserService()

UPLOAD_FOLDER = "uploaded_files" # Directory for profile photos

@router.get("/profile", response_model=UserSchema)
async def get_user_detail(
    current_user: str = Depends(get_current_user),  
    db: Session = Depends(get_db)
):
    user = await UserService.get_user_by_email(current_user, db)
    return user

@router.put("/edit", response_model=UserSchema)
async def update_user_profile(
    user_data: EditUserSchema,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = await UserService.edit_user(db, current_user, user_data)
    return updated_user

@router.post("/upload-profile-photo")
async def upload_or_edit_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """ Upload or edit profile photo (overwrites existing one) """
    return await UserService.upload_or_edit_profile_photo(db, current_user, file)


@router.delete("/delete-profile-photo")
async def delete_photo(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """ Delete profile photo """
    return await UserService.delete_profile_photo(db, current_user)