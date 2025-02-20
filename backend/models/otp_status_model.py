from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.models.base_model import Base

class OTPStatus(Base):
    """
    Stores possible statuses for an OTP, e.g., 'sent', 'not_sent', 'verified'.
    """
    __tablename__ = "otp_status"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(20), unique=True, nullable=False)

    # Relationship to OTPModel
    otps = relationship("OTPModel", back_populates="otp_status")
