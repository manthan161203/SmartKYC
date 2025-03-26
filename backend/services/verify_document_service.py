from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.user_model import User
from backend.models.document_model import Document

class VerifyDocumentService:
    @staticmethod
    def verify_document(db: Session, user_email: str, document_type_id: int):
        """
        Verifies a document by setting `is_verified_document = True`.
        """
        # Fetch user by email
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Fetch the user's document by document_type_id
        document = db.query(Document).filter(
            Document.user_id == user.id,
            Document.document_type_id == document_type_id
        ).first()

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # ✅ Mark document as verified
        document.is_verified_document = True
        db.commit()
        db.refresh(document)

        return {
            "message": f"Document {document_type_id} verified successfully",
            "document_id": document.id,
            "is_verified_document": document.is_verified_document
        }