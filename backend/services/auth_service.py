import re
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from backend.models.user_model import User
from backend.models.gender_type_model import GenderType  # Ensure gender validation
from backend.schemas.auth_schema import ChangePasswordSchema, LoginSchema, RegisterSchema
from backend.utils.security_utils import SecurityUtils

class AuthService:
    async def register_user(self, user_data: RegisterSchema, db: Session):
        """Register a new user with comprehensive error handling."""
        try:
            # Validate required fields
            if not user_data.email or not user_data.phone_number or not user_data.dob:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email, phone number, and date of birth are required."
                )

            # Validate gender_id exists in gender_type table
            gender = db.query(GenderType).filter(GenderType.id == user_data.gender_id).first()
            if not gender:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid gender selection."
                )

            # Check if user already exists
            existing_user = db.query(User).filter(
                (User.email == user_data.email) | (User.phone_number == user_data.phone_number)
            ).first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email or phone number is already registered."
                )

            # Hash the provided password
            hashed_password = SecurityUtils.hash_password(user_data.hashed_password)

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
            if "foreign key constraint" in str(ie.orig).lower():
                error_message = "Invalid reference in the database (e.g., invalid gender ID)."
            elif "duplicate entry" in str(ie.orig).lower():
                error_message = "Email or phone number already exists."
            else:
                error_message = f"Integrity error: {ie.orig.args if ie.orig else str(ie)}"
                
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )

        except SQLAlchemyError as sae:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error occurred: {str(sae)}"
            )

        except ValueError as ve:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid input: {str(ve)}"
            )

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )

    async def login_user(self, login_data: LoginSchema, db: Session):
        """Authenticate user with identifier (email or phone) and password."""
        try:
            identifier = login_data.identifier
            email_regex = r'^\S+@\S+\.\S+$'
            phone_regex = r'^\+?\d{10,15}$'
            
            if re.match(email_regex, identifier):
                user = db.query(User).filter(User.email == identifier).first()
            elif re.match(phone_regex, identifier):
                user = db.query(User).filter(User.phone_number == identifier).first()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid identifier provided."
                )
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials. The provided identifier does not exist."
                )
            
            # Verify password
            if not SecurityUtils.verify_password(login_data.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials. Incorrect password."
                )
            
            return {"message": "Login successful", "user_id": user.id}
        
        except SQLAlchemyError as sae:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"A database error occurred: {str(sae)}"
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )
            
    async def change_password(self, cp_data: ChangePasswordSchema, db: Session):
        """Change user password after verifying current password."""
        try:
            identifier = cp_data.identifier
            email_regex = r'^\S+@\S+\.\S+$'
            phone_regex = r'^\+?\d{10,15}$'
            
            # Determine if identifier is an email or phone
            if re.match(email_regex, identifier):
                user = db.query(User).filter(User.email == identifier).first()
            elif re.match(phone_regex, identifier):
                user = db.query(User).filter(User.phone_number == identifier).first()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid identifier provided."
                )
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )
            
            # Verify the current password
            if not SecurityUtils.verify_password(cp_data.current_password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Current password is incorrect."
                )
            
            # Hash the new password and update
            new_hashed_password = SecurityUtils.hash_password(cp_data.new_password)
            user.hashed_password = new_hashed_password
            
            db.commit()
            db.refresh(user)
            
            return {"message": "Password changed successfully."}
        
        except SQLAlchemyError as sae:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"A database error occurred: {str(sae)}"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )