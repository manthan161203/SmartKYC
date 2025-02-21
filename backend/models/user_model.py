from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.models.base_model import Base

class User(Base):
    """
    User model representing a user in the system.
    Includes profile photo, email/phone verification flags, and relationships.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    dob = Column(DateTime, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    profile_photo = Column(String(255), nullable=True)  # Store photo URL or file path
    is_email_verified = Column(Boolean, default=False, nullable=False)
    is_phone_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Foreign keys for related models (assuming GenderType and KYCStatus exist)
    gender_id = Column(Integer, ForeignKey("gender_type.id"), nullable=False)
    kyc_status_id = Column(Integer, ForeignKey("kyc_status.id"), nullable=True)

    # Relationships
    documents = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    otps = relationship(
        "OTPModel",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    addresses = relationship(
        "UserAddress",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    kyc_status = relationship("KYCStatus", back_populates="users")
    gender = relationship("GenderType", back_populates="users")
