from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Session
from datetime import datetime, timezone
import random
import re
from backend.database.models.document_model import Document
from backend.database.models.base_model import Base
from backend.database.models.enums import OTPStatus, VerificationStatus

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    first_name = Column(String(100), index=True)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    password = Column(String(255))
    
    otp_sent = Column(Enum(OTPStatus), default=OTPStatus.NOT_SENT.value)
    otp_verified = Column(Enum(OTPStatus), default=OTPStatus.NOT_VERIFIED.value)
    otp = Column(String(10), nullable=True)
    otp_expiry = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    address = Column(String(255), nullable=True)
    aadhaar_card_number = Column(String(20), unique=True, nullable=True)
    pan_card_number = Column(String(20), unique=True, nullable=True)
    profile_picture = Column(String(255), nullable=True)
    aadhaar_verified = Column(Enum(VerificationStatus), default=VerificationStatus.NOT_VERIFIED.value)
    pan_verified = Column(Enum(VerificationStatus), default=VerificationStatus.NOT_VERIFIED.value)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    documents = relationship("Document", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
        return bool(pattern.match(phone))

    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        return True