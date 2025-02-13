from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.database.enums import DocumentStatus, DocumentType
from datetime import datetime, timezone

# Document model representing a document uploaded by the user for verification.
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key linking the document to a specific user
    user_id = Column(Integer, ForeignKey("users.id"))  # Refers to 'users' table, column 'id'
    
    # Enum to define the document type (e.g., AADHAAR, PAN, etc.)
    document_type = Column(Enum(DocumentType), default=DocumentType.AADHAAR.value)
    
    document_image_path = Column(String(255))
    
    # Enum to track the verification status of the document (e.g., VERIFIED, NOT_VERIFIED, etc.)
    is_verified = Column(Enum(DocumentStatus), default=DocumentStatus.NOT_VERIFIED.value)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship to the 'User' model, indicating that a document belongs to a specific user
    user = relationship("User", back_populates="documents")

    def __repr__(self):
        # Custom string representation of the Document instance
        return f"<Document(id={self.id}, user_id={self.user_id}, document_type='{self.document_type}')>"
