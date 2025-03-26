import json
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.document_model import Document
from backend.models.document_details_model import DocumentDetails

class ExtractDetailsService:
    @staticmethod
    def extract_details(db: Session, user_id: int, document_type_id: int):
        """
        Extract stored document details for a specific user and document type.
        """
        # Fetch the document for the user with the given document type
        document = db.query(Document).filter(
            Document.user_id == user_id,
            Document.document_type_id == document_type_id
        ).first()

        if not document:
            raise HTTPException(status_code=404, detail="Document not found for this user and type")

        # Fetch document details
        doc_details = db.query(DocumentDetails).filter(DocumentDetails.document_id == document.id).first()
        if not doc_details:
            raise HTTPException(status_code=404, detail="No extracted details found for this document")

        try:
            # Parse stored JSON details
            details_data = json.loads(doc_details.details)
        except json.JSONDecodeError:
            details_data = "Error parsing stored data"

        return {
            "user_id": user_id,
            "document_type_id": document_type_id,
            "document_details": details_data
        }