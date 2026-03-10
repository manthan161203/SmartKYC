import os
import uuid
import shutil

UPLOAD_ROOT = os.path.abspath("uploaded_files")

def upload_profile_photo(file, user_id: int) -> str:
    """
    Uploads a profile photo to local storage and returns the relative path.
    """
    file_extension = file.filename.split(".")[-1]
    unique_file_name = f"{uuid.uuid4()}.{file_extension}"
    relative_path = os.path.join("profiles", str(user_id), unique_file_name)
    full_path = os.path.join(UPLOAD_ROOT, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return relative_path


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
    Removes a profile photo from local storage.
    """
    full_path = os.path.join(UPLOAD_ROOT, photo_path)
    if os.path.exists(full_path):
        os.remove(full_path)
    return True
