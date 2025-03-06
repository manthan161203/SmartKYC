from sqlalchemy.orm import Session
from backend.models.document_model import Document
from backend.utils.supabase_document_upload_utils import upload_image_to_supabase
from backend.schemas.document_schema import DocumentUploadRequest, DocumentResponse

def upload_user_document(db: Session, request: DocumentUploadRequest, file, file_name: str) -> DocumentResponse:
    """
    Uploads a user document to Supabase, stores (or replaces) the link in the database, and returns the document details.
    
    If a document with the same user_id and document_type_id exists, it replaces the existing file URL.
    """
    # Upload file to Supabase and get the new file URL
    file_url = upload_image_to_supabase(file, file_name)
    
    # Check if a document already exists for this user and document type
    existing_document = (
        db.query(Document)
        .filter(
            Document.user_id == request.user_id,
            Document.document_type_id == request.document_type_id
        )
        .first()
    )
    
    if existing_document:
        # Replace the existing file path with the new URL
        existing_document.file_path = file_url
        db.commit()
        db.refresh(existing_document)
        document = existing_document
    else:
        # Create a new document record if none exists
        new_document = Document(
            user_id=request.user_id,
            document_type_id=request.document_type_id,
            file_path=file_url
        )
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        document = new_document

    return DocumentResponse(
        id=document.id,
        user_id=document.user_id,
        document_type_id=document.document_type_id,
        file_path=document.file_path,
        is_verified_document=document.is_verified_document
    )
