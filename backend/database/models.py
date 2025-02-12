from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, MetaData, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

class DocumentStatus(PyEnum):
    NOT_VERIFIED = "not_verified"
    VERIFIED = "verified"
    PENDING = "pending"

class OTPStatus(PyEnum):
    SENT = "sent"
    VERIFIED = "verified"
    EXPIRED = "expired"

metadata = MetaData()

Base = declarative_base(metadata=metadata)

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
    
    is_document_verified = Column(Enum(DocumentStatus), default=DocumentStatus.NOT_VERIFIED)
    
    otp_sent = Column(Enum(OTPStatus), default=OTPStatus.SENT)
    otp_verified = Column(Enum(OTPStatus), default=OTPStatus.SENT)
    otp = Column(String(10), nullable=True)
    otp_expiry = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    address = Column(String(255), nullable=True)

    aadhaar_card_number = Column(String(20), nullable=True)
    pan_card_number = Column(String(20), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    
    aadhaar_verified = Column(Boolean, default=False)
    pan_verified = Column(Boolean, default=False)
    
    documents = relationship("Document", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    document_type = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING)
    document_image_path = Column(String(255))
    
    is_verified = Column(Enum(DocumentStatus), default=DocumentStatus.NOT_VERIFIED)
    
    user = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"Document(id={self.id}, user_id={self.user_id}, document_type={self.document_type})"
