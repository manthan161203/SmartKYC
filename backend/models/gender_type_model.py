from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.models.base_model import Base

class GenderType(Base):
    """
    Model representing a type of gender.
    """
    __tablename__ = "gender_type"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), unique=True, nullable=False)

    # Relationship: A gender type can be associated with many users.
    users = relationship("User", back_populates="gender")
