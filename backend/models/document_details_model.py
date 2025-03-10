from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from backend.models.base_model import Base

class DocumentDetails(Base):
    """
    Document Details table storing additional details in JSON format related to user documents.
    """
    __tablename__ = "document_details"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    details = Column(JSON, nullable=True)  # Stores document details in JSON format
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    document = relationship("Document", back_populates="document_details")
