import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from backend.config.config import settings

# Cloudinary Configuration
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_image_to_cloudinary(file):
    """
    Uploads an image to Cloudinary and returns the optimized secure URL.
    """
    upload_result = cloudinary.uploader.upload(file)

    # Get the uploaded image's public ID
    public_id = upload_result.get("public_id")

    # Generate an optimized URL
    optimized_url, _ = cloudinary_url(public_id, fetch_format="auto", quality="auto")

    return optimized_url
