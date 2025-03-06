import os
from supabase import create_client
from backend.config.config import settings
import uuid

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_image_to_supabase(file, file_name: str):
    """
    Uploads an image to Supabase Storage using file_options and returns the public URL.
    """
    bucket_name = "documents"  # Ensure this bucket exists in Supabase

    # Print for debugging purposes
    print(file, file_name)
    
    # Generate a unique file path (using uuid for uniqueness)
    unique_file_name = f"{uuid.uuid4()}_{file_name}"
    file_path = f"uploads/{unique_file_name}"

    # Read the file bytes from the SpooledTemporaryFile
    file_bytes = file.read()

    # Upload file to Supabase with specified file options
    upload_response = supabase.storage.from_(bucket_name).upload(
        path=file_path,
        file=file_bytes,
        file_options={"cache-control": "3600", "upsert": "false"}
    )
    
    print("Upload response:", upload_response)
    
    # Get the public URL using Supabase's get_public_url method with file options
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path, {"download": True})
    
    print("Public URL:", public_url)
    
    return public_url
