from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.schemas.document_schema import DocumentUploadRequest, DocumentResponse
from backend.services.document_service import upload_user_document

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    user_id: int,
    document_type_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Uploads a document image to Supabase and stores the link in the database.
    """
    request = DocumentUploadRequest(user_id=user_id, document_type_id=document_type_id)
    document = upload_user_document(db, request, file.file, file.filename)
    return document
