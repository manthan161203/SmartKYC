from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.database.enums import DocumentStatus, DocumentType
from datetime import datetime, timezone

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    document_type = Column(Enum(DocumentType), nullable=False)
    document_image_path = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"<Document(id={self.id}, user_id={self.user_id}, document_type='{self.document_type}')>"
