from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.models.base_model import Base

class KYCStatus(Base):
    """
    KYCStatus model to track the overall KYC verification status of a user.
    Possible statuses might include 'Pending', 'Verified', or 'Rejected'.
    """
    __tablename__ = "kyc_status"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), unique=True, nullable=False)
    
    # Relationship: One KYC status can be associated with many users.
    users = relationship("User", back_populates="kyc_status")
