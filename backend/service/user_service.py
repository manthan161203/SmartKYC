from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.database.models.enums import OTPStatus
from backend.database.models.user_model import User
from backend.schemas.user_schema import UserCreate
from backend.service.auth_service import hash_password
from backend.service.otp_service import send_otp_email, validate_otp

def register_user(user: UserCreate, db: Session):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if not User.validate_phone(user.phone):
        raise HTTPException(status_code=400, detail="Invalid phone number format")

    if not User.validate_password(user.password):
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, and a number.")
    
    hashed_password = hash_password(user.password)
    
    new_user = User(
        first_name=user.first_name,
        middle_name=user.middle_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        address=user.address,
        aadhaar_card_number=user.aadhaar_card_number,
        pan_card_number=user.pan_card_number,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    send_otp_email(new_user.email, db)
    
    return {"message": "User registered successfully", "user_id": new_user.id}

def validate_otp_user(email: str, otp: str, db: Session):
    if validate_otp(email, otp, db):
        user = db.query(User).filter(User.email == email).first()
        user.otp_verified = OTPStatus.VERIFIED.value
        db.commit()
        return {"message": "OTP validated successfully"}
    
    raise HTTPException(status_code=400, detail="OTP validation failed")
