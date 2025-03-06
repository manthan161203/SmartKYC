import uuid
from supabase import create_client
from sqlalchemy.orm import Session
from backend.config.config import settings
from backend.models.document_type_model import DocumentType

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_document_type_by_id(db: Session, document_type_id: int) -> str:
    """
    Fetch document type name by ID.
    """
    document_type = db.query(DocumentType).filter(DocumentType.id == document_type_id).first()
    return document_type.name if document_type else "other"

def remove_existing_files_in_folder(user_id: str, document_type_name: str):
    """
    Removes all files inside the document type folder before uploading a new one.
    Example folder structure: uploads/{user_id}/{document_type_name}/
    """
    bucket_name = "documents"
    folder_path = f"uploads/{user_id}/{document_type_name}/"

    # List all files in the folder
    list_response = supabase.storage.from_(bucket_name).list(folder_path)

    if not list_response:
        return  # No files to delete

    # Extract file paths to delete
    files_to_delete = [f"{folder_path}{file['name']}" for file in list_response]

    if files_to_delete:
        # Remove all files
        delete_response = supabase.storage.from_(bucket_name).remove(files_to_delete)
        if not delete_response:
            raise Exception("Failed to remove existing files from Supabase")

def upload_image_to_supabase(db: Session, file, file_name: str, user_id: str, document_type_id: int) -> str:
    """
    Uploads a document to Supabase Storage and returns its public URL.
    The document is stored in a user-specific folder structure:
    uploads/{user_id}/{document_type_name}/{unique_file_name}
    """
    bucket_name = "documents"

    # Get document type name
    document_type_name = get_document_type_by_id(db, document_type_id)

    # Remove existing files in the folder before uploading the new one
    remove_existing_files_in_folder(user_id, document_type_name)

    # Generate a unique file name
    unique_file_name = f"{uuid.uuid4()}_{file_name}"
    file_path = f"uploads/{user_id}/{document_type_name}/{unique_file_name}"

    # Read file bytes
    file_bytes = file.read()

    # Upload file to Supabase
    upload_response = supabase.storage.from_(bucket_name).upload(
        path=file_path,
        file=file_bytes,
        file_options={"cache-control": "3600", "upsert": "false"}
    )

    if not upload_response:
        raise Exception("Failed to upload file to Supabase")

    # Get the public URL
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path, {"download": True})
    
    return public_url
