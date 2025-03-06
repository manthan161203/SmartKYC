from sqlalchemy.orm import Session
from backend.models.document_model import Document
from backend.schemas.document_schema import DocumentUploadRequest, DocumentResponse
from backend.utils.supabase_document_upload_utils import upload_image_to_supabase

def upload_user_document(db: Session, request: DocumentUploadRequest, file, file_name: str) -> DocumentResponse:
    """
    Uploads a user document to Supabase, removes old files in the folder, 
    stores the latest link in the database, and returns document details.
    """
    # Upload the new document (old files are deleted inside this function)
    file_url = upload_image_to_supabase(db, file, file_name, request.user_id, request.document_type_id)

    # Check if an existing document record is there
    existing_document = (
        db.query(Document)
        .filter(
            Document.user_id == request.user_id,
            Document.document_type_id == request.document_type_id
        )
        .first()
    )

    if existing_document:
        existing_document.file_path = file_url
        db.commit()
        db.refresh(existing_document)
        document = existing_document
    else:
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
