from sqlalchemy.orm import Session
from backend.models.document_details_model import DocumentDetails
from backend.models.document_model import Document
from backend.schemas.document_schema import DocumentUploadRequest, DocumentResponse, DocumentProcessingResponse
from backend.utils.get_document_from_supabase import get_document_type_by_id, get_user_document
from backend.utils.supabase_document_upload_utils import upload_image_to_supabase
from backend.utils.image_processing_ocr import process_image
from backend.utils.openai_utils import build_prompt, query_openai, remove_markdown

import json

def upload_user_document(db: Session, request: DocumentUploadRequest, file, file_name: str) -> DocumentResponse:
    """
    Uploads a user document to Supabase, removes old files in the folder, 
    stores the latest link in the database, and returns document details.
    """
    file_url = upload_image_to_supabase(db, file, file_name, request.user_id, request.document_type_id)

    existing_document = (
        db.query(Document)
        .filter(Document.user_id == request.user_id, Document.document_type_id == request.document_type_id)
        .first()
    )

    if existing_document:
        existing_document.file_path = file_url
        db.commit()
        db.refresh(existing_document)
        document = existing_document
    else:
        new_document = Document(user_id=request.user_id, document_type_id=request.document_type_id, file_path=file_url)
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

def fetch_user_document(db: Session, user_id: int, document_type_id: int) -> str:
    """
    Fetches the latest document URL for a user.
    """
    return get_user_document(db, user_id, document_type_id)


def process_user_document(db: Session, user_id: int, document_type_id: int) -> DocumentProcessingResponse:
    """
    Fetches the latest document URL from Supabase, extracts text using OCR & OpenAI, 
    and stores structured data in the document_details table.
    """
    # Get the latest document URL from Supabase
    document_url = get_user_document(db, user_id, document_type_id)

    # Process image and extract text
    ocr_json = process_image(document_url)
    
    # Fetch document type name for the prompt
    document_type = get_document_type_by_id(db, document_type_id)
    
    # Generate OpenAI prompt based on document type
    prompt = build_prompt(ocr_json, side=document_type)
    openai_response = query_openai(prompt)
    print(f"OpenAI Response: {openai_response}")
    if not openai_response:
        raise ValueError("OpenAI response is empty or None")
    try:
        extracted_data = json.loads(remove_markdown(openai_response))
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
    
    extracted_data = {}

    extracted_data = json.loads(remove_markdown(openai_response))

    # Find the document in the DB
    document = (
        db.query(Document)
        .filter(Document.user_id == user_id, Document.document_type_id == document_type_id)
        .first()
    )
    if not document:
        raise ValueError("Document not found in the database.")

    # Check if details already exist
    existing_details = db.query(DocumentDetails).filter(DocumentDetails.document_id == document.id).first()

    if existing_details:
        existing_details.details = extracted_data
        db.commit()
        db.refresh(existing_details)
    else:
        new_details = DocumentDetails(document_id=document.id, details=extracted_data)
        db.add(new_details)
        db.commit()
        db.refresh(new_details)

    return DocumentProcessingResponse(document_id=document.id, extracted_data=extracted_data)
