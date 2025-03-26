import os
import shutil
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from backend.models.user_model import User
from backend.models.user_address_model import UserAddress
from backend.schemas.user_schema import EditUserSchema

UPLOAD_FOLDER = "uploaded_files"

class UserService:
    @staticmethod
    async def get_user_by_email(email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def edit_user(db: Session, email: str, user_data: EditUserSchema):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Prevent KYC status modification
        if "kyc_status_id" in user_data.model_dump():
            raise HTTPException(status_code=400, detail="KYC status cannot be changed.")

        # Check if email is unique
        if user_data.email and user_data.email != user.email:
            existing_email = db.query(User).filter(User.email == user_data.email).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="Email is already in use.")

        # Check if phone number is unique
        if user_data.phone_number and user_data.phone_number != user.phone_number:
            existing_phone = db.query(User).filter(User.phone_number == user_data.phone_number).first()
            if existing_phone:
                raise HTTPException(status_code=400, detail="Phone number is already in use.")

        # Update user fields
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        # Handle address updates
        address_fields = ["address_line1", "address_line2", "city", "state", "country", "postal_code"]
        if any(field in update_data for field in address_fields):
            address = db.query(UserAddress).filter(UserAddress.user_id == user.id).first()
            if not address:
                address = UserAddress(user_id=user.id)
                db.add(address)

            for key, value in update_data.items():
                if hasattr(address, key):
                    setattr(address, key, value)

        db.commit()
        db.refresh(user)
        
        return user

    @staticmethod
    async def upload_or_edit_profile_photo(db: Session, email: str, file: UploadFile):
        """ Upload or update (edit) the user's profile photo """

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Ensure user folder exists
        user_folder = os.path.join(UPLOAD_FOLDER, str(user.id))
        os.makedirs(user_folder, exist_ok=True)

        # Get file extension and validate
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["jpg", "jpeg", "png", "gif"]:
            raise HTTPException(status_code=400, detail="Invalid file format. Only JPG, JPEG, PNG, and GIF allowed.")

        # Define new file path (relative)
        new_file_name = f"profile_photo.{file_ext}"
        new_file_path = os.path.join(user_folder, new_file_name)

        # Delete old profile photo if it exists
        if user.profile_photo:
            old_photo_path = os.path.join(UPLOAD_FOLDER, user.profile_photo)
            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)

        # Save new file
        with open(new_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Update database with relative path
        relative_path = f"{str(user.id)}/{new_file_name}"  # Store "1/profile_photo.jpg"
        user.profile_photo = relative_path
        db.commit()
        db.refresh(user)

        # Return full URL for frontend
        full_photo_url = f"http://localhost:8000/uploads/{relative_path}"
        return {"message": "Profile photo uploaded/updated successfully", "photo_url": full_photo_url}

    @staticmethod
    async def delete_profile_photo(db: Session, email: str):
        """ Delete the user's profile photo """

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.profile_photo:
            raise HTTPException(status_code=400, detail="No profile photo found.")

        # Remove file from system
        photo_path = os.path.join(UPLOAD_FOLDER, user.profile_photo)
        if os.path.exists(photo_path):
            os.remove(photo_path)

        # Update database
        user.profile_photo = None
        db.commit()
        db.refresh(user)

        return {"message": "Profile photo deleted successfully"}