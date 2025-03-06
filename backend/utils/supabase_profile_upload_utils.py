import uuid
from supabase import create_client
from backend.config.config import settings

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

BUCKET_NAME = "profile_photos"

def upload_profile_photo(file, user_id: int) -> str:
    """
    Uploads a profile photo to Supabase and returns the public URL.
    """
    file_extension = file.filename.split(".")[-1]
    unique_file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"profiles/{user_id}/{unique_file_name}"

    # Read file bytes
    file_bytes = file.file.read()

    # Upload file to Supabase
    response = supabase.storage.from_(BUCKET_NAME).upload(
        path=file_path,
        file=file_bytes,
        file_options={"cache-control": "3600", "upsert": "false"}
    )

    if not response:
        raise Exception("Failed to upload profile photo to Supabase")

    # Get the public URL
    return supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)


def update_profile_photo(file, user_id: int, old_photo_path: str) -> str:
    """
    Updates the profile photo by deleting the old one and uploading a new one.
    """
    # Remove the old photo
    if old_photo_path:
        remove_profile_photo(old_photo_path)

    # Upload new photo
    return upload_profile_photo(file, user_id)


def remove_profile_photo(photo_path: str) -> bool:
    """
    Removes a profile photo from Supabase storage.
    """
    response = supabase.storage.from_(BUCKET_NAME).remove([photo_path])

    if response.get("error"):
        raise Exception("Failed to remove profile photo from Supabase")

    return True
