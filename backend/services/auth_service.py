import re
import redis
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.config.config import settings
from backend.models.user_model import User
from backend.models.gender_type_model import GenderType
from backend.models.otp_model import OTPModel
from backend.schemas.auth_schema import ChangePasswordSchema, RegisterSchema
from backend.schemas.otp_schema import VerifyOTPSchema
from backend.utils.otp_email_utils import send_email
from backend.utils.security_utils import SecurityUtils
from backend.utils.token_utils import TokenUtils

EMAIL_REGEX = re.compile(r'^\S+@\S+\.\S+$')
PHONE_REGEX = re.compile(r'^\+?\d{10,15}$')

REDIS_CLIENT = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class AuthService:
    @staticmethod
    async def register_user(user_data: RegisterSchema, db: Session):
        try:
            if not db.query(GenderType).filter(GenderType.id == user_data.gender_id).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid gender selection.")
                        
            hashed_password = SecurityUtils.hash_password(user_data.password)

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

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")

    @staticmethod
    async def login_user(form_data: OAuth2PasswordRequestForm, db: Session):
        """Authenticate user and generate OTP for login."""
        try:
            identifier = form_data.username

            user = db.query(User).filter(
                or_(User.email == identifier, User.phone_number == identifier)
            ).first()

            if not user or not SecurityUtils.verify_password(form_data.password, user.hashed_password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

            access_token = TokenUtils.generate_token(identifier=user.email, purpose="auth")
            print(f"Access token: {access_token}")
            return {
                "message": "Login successful. OTP sent to your registered email/phone.",
                "access_token": access_token,
                "token_type": "Bearer"
            }
            
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred.")
        
    @staticmethod
    async def generate_and_store_otp(current_user: str, db: Session):
        """Generate and store OTP for a user, with the option of using Redis or SQL database."""
        try:
            
            user = db.query(User).filter(User.email == current_user).first()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")

             # Fetch user's full name
            full_name = user.full_name
            
            # Generate new OTP
            otp_code = SecurityUtils.generate_otp()
            
            # Get OTP expiry time from settings use when storing OTP in Redis
            otp_expiry_seconds = settings.OTP_EXPIRY_TIME
            
            REDIS_CLIENT.setex(f"otp:{user.id}", otp_expiry_seconds, otp_code)
            
            # Send OTP via email
            email_sent = send_email(user.email, full_name, "otp", otp_code)
            if not email_sent:
                raise HTTPException(status_code=500, detail="Failed to send OTP via email.")

            return {"message": "OTP generated and sent successfully", "otp": otp_code}  # Remove OTP from response in production.

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    @staticmethod
    async def resend_otp(current_user: str, db: Session):
        """Resend OTP to user's email or phone number."""
        try:
            user = db.query(User).filter(User.email == current_user).first()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")

            # Fetch user's full name
            full_name = user.full_name

            # Generate new OTP
            otp_code = SecurityUtils.generate_otp()

            # Get OTP expiry time from settings use when storing OTP in Redis
            otp_expiry_seconds = settings.OTP_EXPIRY_TIME

            REDIS_CLIENT.setex(f"otp:{user.id}", otp_expiry_seconds, otp_code)

            # Send OTP via email
            email_sent = send_email(user.email, full_name, "otp", otp_code)
            if not email_sent:
                raise HTTPException(status_code=500, detail="Failed to send OTP via email.")
            
            return {"message": "OTP resent successfully", "otp": otp_code}  # Remove OTP from response in production.
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def verify_otp(otp_data: VerifyOTPSchema, db: Session, current_user: str):
        """Verify OTP for a user, with the option of using Redis or SQL database."""

        try:
            user = db.query(User).filter(User.email == current_user).first()
            
            if not user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found.")
        
            stored_otp = REDIS_CLIENT.get(f"otp:{user.id}")

            if stored_otp is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found or expired.")

            if isinstance(stored_otp, bytes):
                stored_otp = stored_otp.decode("utf-8")

            if stored_otp != otp_data.otp_code:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP.")

            REDIS_CLIENT.delete(f"otp:{user.id}")
            
            return {"message": "OTP verified successfully. You are now logged in."}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def verify_email(current_user: str, db: Session):
        """Verify user email address."""
        try:
            user = db.query(User).filter(User.email == current_user).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")

            user.is_email_verified = True
            db.commit()
            return {"message": "Email verified successfully."}

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred.")

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    @staticmethod
    async def forgot_password(email: str, db: Session):
        """
        Generate a reset password token and send the reset link via email.
        """
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate reset token (valid for 30 minutes)
        reset_token = TokenUtils.generate_token(user.email, "reset_password", expires_in=30)

        # Construct password reset link
        reset_link = f"http://localhost:5173/reset-password?token={reset_token}"

        # Send email using the email utility
        email_sent = send_email(
            to_email=user.email,
            full_name=user.full_name,
            email_type="reset_password",
            reset_link=reset_link
        )

        if not email_sent:
            raise HTTPException(status_code=500, detail="Failed to send password reset email")

        return {"message": "Password reset email sent successfully."}

    @staticmethod
    async def reset_password(token: str, new_password: str, db: Session):
        """
        Verify reset token and update the user's password.
        """
        # Validate the token
        try:
            email = TokenUtils.verify_token(token, "reset_password")
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

        # Find the user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        print(f"User found: {user.full_name}")
        print(f"New password: {new_password}")
        
        # Hash the new password using SecurityUtils
        hashed_password = SecurityUtils.hash_password(new_password)

        # Update password
        user.hashed_password = hashed_password
        db.commit()

        return {"message": "Password reset successful."}
    
    @staticmethod
    async def change_password(cp_data: ChangePasswordSchema, email: str, db: Session):
        """Change user password after verifying current password."""
        try:
            user = db.query(User).filter(User.email == email).first()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

            if not SecurityUtils.verify_password(cp_data.current_password, user.hashed_password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is incorrect.")

            user.hashed_password = SecurityUtils.hash_password(cp_data.new_password)
            db.commit()
            db.refresh(user)

            return {"message": "Password changed successfully."}

        except HTTPException as http_exc:
            raise http_exc

        except SQLAlchemyError as sae:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error occurred: {str(sae)}")

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")