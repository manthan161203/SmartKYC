from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.schemas.document_schema import DocumentUploadRequest, DocumentResponse, DocumentProcessingResponse
from backend.services.document_service import fetch_user_document, upload_user_document, process_user_document

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    user_id: int,
    document_type_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Uploads a document to local storage and stores the path in the database.
    """
    request = DocumentUploadRequest(user_id=user_id, document_type_id=document_type_id)
    document = upload_user_document(db, request, file.file, file.filename)
    return document

@router.get("/get")
def get_document(user_id: int, document_type_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the latest uploaded document URL for a given user.
    """
    document_url = fetch_user_document(db, user_id, document_type_id)
    return {"document_url": document_url}

@router.post("/process", response_model=DocumentProcessingResponse)
def process_document(user_id: int, document_type_id: int, db: Session = Depends(get_db)):
    """
    Processes the latest document for the given user, extracts structured data, 
    and saves it in the document_details table.
    """
    processed_data = process_user_document(db, user_id, document_type_id)
    return processed_data
