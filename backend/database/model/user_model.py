from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.database.enums import DocumentStatus, OTPStatus
from datetime import datetime, timezone

# User model representing a user in the KYC system.
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
    is_document_verified = Column(Enum(DocumentStatus), default=DocumentStatus.NOT_VERIFIED.value)
    
    # OTP status for sent and verified, defaults to 'SENT'
    otp_sent = Column(Enum(OTPStatus), default=OTPStatus.SENT.value)
    otp_verified = Column(Enum(OTPStatus), default=OTPStatus.SENT.value)
    otp = Column(String(10), nullable=True)
    otp_expiry = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    address = Column(String(255), nullable=True)
    aadhaar_card_number = Column(String(20), unique=True, nullable=True)
    pan_card_number = Column(String(20), unique=True, nullable=True)
    profile_picture = Column(String(255), nullable=True)
    aadhaar_verified = Column(Boolean, default=False)
    pan_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship with the Document model. A user can have multiple documents.
    documents = relationship("Document", back_populates="user", cascade="all, delete")

    def __repr__(self):
        # Custom string representation of the Document instance
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
