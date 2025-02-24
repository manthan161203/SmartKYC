import re
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.models.user_model import User
from backend.models.gender_type_model import GenderType
from backend.schemas.auth_schema import ChangePasswordSchema, LoginSchema, RegisterSchema
from backend.utils.security_utils import SecurityUtils

# Precompiled regex patterns for validation
EMAIL_REGEX = re.compile(r'^\S+@\S+\.\S+$')
PHONE_REGEX = re.compile(r'^\+?\d{10,15}$')


class AuthService:
    @staticmethod
    async def register_user(user_data: RegisterSchema, db: Session):
        """Register a new user with robust error handling."""
        try:
            # Ensure gender_id is valid
            if not db.query(GenderType).filter(GenderType.id == user_data.gender_id).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid gender selection.")

            # Check if email or phone number is already registered
            existing_user = db.query(User).filter(
                or_(User.email == user_data.email, User.phone_number == user_data.phone_number)
            ).first()

            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or phone number already registered.")

            # Hash the password
            hashed_password = SecurityUtils.hash_password(user_data.password)

            # Create new user
            new_user = User(
                full_name=user_data.full_name,
                email=user_data.email,
                phone_number=user_data.phone_number,
                dob=user_data.dob,
                gender_id=user_data.gender_id,
                hashed_password=hashed_password
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {"message": "User registered successfully", "user_id": new_user.id}

        except IntegrityError as ie:
            db.rollback()
            error_message = str(ie.orig).lower()
            if "duplicate entry" in error_message or "unique constraint" in error_message:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or phone number already exists.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database constraint error.")

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred.")

        except Exception:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

    @staticmethod
    async def login_user(login_data: LoginSchema, db: Session):
        """Authenticate user using email or phone number and password."""
        try:
            identifier = login_data.identifier

            # Find user by email or phone number
            user = db.query(User).filter(
                or_(User.email == identifier, User.phone_number == identifier)
            ).first()

            if not user or not SecurityUtils.verify_password(login_data.password, user.hashed_password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

            return {"message": "Login successful", "user_id": user.id}

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred.")

        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

    @staticmethod
    async def change_password(cp_data: ChangePasswordSchema, db: Session):
        """Change user password after verifying current password."""
        try:
            identifier = cp_data.identifier

            # Find user by email or phone number
            user = db.query(User).filter(
                or_(User.email == identifier, User.phone_number == identifier)
            ).first()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

            # Verify the current password
            if not SecurityUtils.verify_password(cp_data.current_password, user.hashed_password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is incorrect.")

            # Hash the new password and update
            user.hashed_password = SecurityUtils.hash_password(cp_data.new_password)
            db.commit()
            db.refresh(user)

            return {"message": "Password changed successfully."}

        except HTTPException as http_exc:
            # If the error is an HTTPException (e.g., invalid current password), propagate it
            raise http_exc

        except SQLAlchemyError as sae:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error occurred: {str(sae)}")

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
