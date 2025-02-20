from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.models.base_model import Base

class DocumentType(Base):
    """
    Stores types of documents (e.g., Aadhar, PAN, Selfie, etc.).
    """
    __tablename__ = "document_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # Relationship to Document
    documents = relationship("Document", back_populates="document_type")
