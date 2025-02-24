from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.models.base_model import Base

class OTPModel(Base):
    """
    OTP model to store one-time passwords for users.
    """
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    otp = Column(String(10), nullable=False)
    expiry = Column(DateTime, nullable=False, default=lambda: datetime.now(tz=timezone.utc) + timedelta(minutes=10))
    otp_status_id = Column(Integer, ForeignKey("otp_status.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="otps")
    otp_status = relationship("OTPStatus", back_populates="otps")
