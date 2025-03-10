from supabase import create_client
from sqlalchemy.orm import Session
from backend.config.config import settings
from backend.models.document_model import Document
from backend.models.document_type_model import DocumentType

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_document_type_by_id(db: Session, document_type_id: int) -> str:
    """
    Fetch document type name by ID.
    """
    document_type = db.query(DocumentType).filter(DocumentType.id == document_type_id).first()
    return document_type.name if document_type else "other"

def get_user_document(db: Session, user_id: int, document_type_id: int) -> str:
    """
    Retrieves the latest uploaded document URL for a given user and document type.
    """
    bucket_name = "documents"

    # Get document type name
    document_type_name = get_document_type_by_id(db, document_type_id)

    # Construct folder path
    folder_path = f"uploads/{user_id}/{document_type_name}/"

    # List files in the user's document folder
    list_response = supabase.storage.from_(bucket_name).list(folder_path)

    if not list_response:
        raise Exception("No documents found for the user.")

    # Sort files by name (assuming filename contains timestamp or UUID for ordering)
    list_response.sort(key=lambda x: x["name"], reverse=True)

    # Get the latest file
    latest_file = list_response[0]["name"]
    file_path = f"{folder_path}{latest_file}"

    # Generate the public URL
    signed_url_response = supabase.storage.from_(bucket_name).create_signed_url(file_path, expires_in=86400)  # Expires in 1 day
    document_url = signed_url_response["signedURL"]

    return document_url
