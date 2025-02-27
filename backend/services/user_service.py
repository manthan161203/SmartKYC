from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.user_model import User
from backend.models.user_address_model import UserAddress
from backend.schemas.user_schema import EditUserSchema

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
