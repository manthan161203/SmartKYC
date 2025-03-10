from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.models.base_model import Base
from backend.models.document_details_model import DocumentDetails

class Document(Base):
    """
    Document table storing user documents.
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    document_type_id = Column(Integer, ForeignKey("document_type.id"), nullable=False)
    file_path = Column(String(255), nullable=False)
    is_verified_document = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="documents")
    document_type = relationship("DocumentType", back_populates="documents")
    document_details = relationship("DocumentDetails", back_populates="document", cascade="all, delete-orphan")
