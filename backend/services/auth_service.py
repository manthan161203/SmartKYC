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
from backend.schemas.otp_schema import UserOTPSchema, VerifyOTPSchema
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

            otp_response = await AuthService.generate_and_store_otp(user.id, db)
            access_token = TokenUtils.generate_token(identifier=user.email, purpose="auth")

            return {
                "message": "Login successful. OTP sent to your registered email/phone.",
                "user_id": user.id,
                "otp_message": otp_response["message"],
                "access_token": access_token,
                "token_type": "Bearer"
            }
            
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred.")
        
    @staticmethod
    async def generate_and_store_otp(otp_send_data: UserOTPSchema, db: Session):
        """Generate and store OTP for a user, with the option of using Redis or SQL database."""
        try:
            
            user_id = otp_send_data
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")

             # Fetch user's full name
            full_name = user.full_name
            # Uncomment this section to use SQL-based OTP generation (old logic)
            # Delete all OTPs related to this user_id
            # db.query(OTPModel).filter(OTPModel.user_id == user_id).delete(synchronize_session=False)

            # Generate new OTP
            otp_code = SecurityUtils.generate_otp()
            
            # Get OTP expiry time from settings use when storing OTP in Redis
            otp_expiry_seconds = settings.OTP_EXPIRY_TIME
            
            # Uncomment this section to use OTP expiry time from the database
            # otp_expiry = SecurityUtils.get_otp_expiry()
            

            # Uncomment this section to use SQL-based OTP generation (old logic)
            # Store new OTP
            # otp_entry = OTPModel(user_id=user_id, otp=otp_code, expiry=otp_expiry, otp_status_id=2)  # Status: Sent
            # db.add(otp_entry)
            # db.commit()
            # db.refresh(otp_entry)

            # Store OTP in Redis (Auto-expires in 10 minutes)
            REDIS_CLIENT.setex(f"otp:{user_id}", otp_expiry_seconds, otp_code)
            
            # Uncomment this section to use SQL-based OTP generation (old logic)
            # Send OTP via email
            # email_sent = send_email(user.email, full_name, "otp", otp_code)
            # if not email_sent:
            #     raise HTTPException(status_code=500, detail="Failed to send OTP via email.")

            return {"message": "OTP generated and sent successfully", "otp": otp_code}  # Remove OTP from response in production.

        # Uncomment this section to use SQL-based OTP generation (old logic)
        # except SQLAlchemyError:
        #     db.rollback()
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Failed to generate OTP. Please try again later."
        #     )

        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(
        #         status_code=500,
        #         detail=f"An unexpected error occurred: {str(e)}"
        #     )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    @staticmethod
    async def verify_otp(otp_data: VerifyOTPSchema, db: Session):
        """Verify OTP for a user, with the option of using Redis or SQL database."""

        # Uncomment this section to use SQL-based OTP verification (old logic)
        # try:
        #     otp_entry = (
        #         db.query(OTPModel)
        #         .filter(OTPModel.user_id == otp_data.user_id, OTPModel.otp_status_id == 2)  # OTP Status: Sent
        #         .order_by(OTPModel.expiry.desc())
        #         .first()
        #     )
        #
        #     if not otp_entry:
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found.")
        #
        #     if otp_entry.otp != otp_data.otp_code:
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP.")
        #
        #     if datetime.now(tz=timezone.utc) > otp_entry.expiry.replace(tzinfo=timezone.utc):
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired.")
        #
        #     otp_entry.otp_status_id = 3  # Status: Verified
        #     db.commit()
        #
        #     return {"message": "OTP verified successfully. You are now logged in."}
        #
        # except SQLAlchemyError:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred.")
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

        try:
            stored_otp = REDIS_CLIENT.get(f"otp:{otp_data.user_id}")

            if stored_otp is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found or expired.")

            if isinstance(stored_otp, bytes):
                stored_otp = stored_otp.decode("utf-8")

            if stored_otp != otp_data.otp_code:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP.")

            REDIS_CLIENT.delete(f"otp:{otp_data.user_id}")
            
            return {"message": "OTP verified successfully. You are now logged in."}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    async def change_password(cp_data: ChangePasswordSchema, db: Session):
        """Change user password after verifying current password."""
        try:
            identifier = cp_data.identifier

            user = db.query(User).filter(
                or_(User.email == identifier, User.phone_number == identifier)
            ).first()

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