from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.config.database import get_db
from backend.services.verify_document_service import VerifyDocumentService
from backend.utils.jwt_middleware import get_current_user

router = APIRouter(prefix="/verify_document", tags=["Verify Document"])

# ✅ Request Model for Verification
class VerifyDocumentRequest(BaseModel):
    document_type_id: int  # Only document_type_id needed, user info from current_user

@router.patch("/")
def verify_document(
    request: VerifyDocumentRequest,
    current_user: str = Depends(get_current_user),  # Get user email from token
    db: Session = Depends(get_db)
):
    """
    API to verify a document. Sets `is_verified_document = True`.
    """
    return VerifyDocumentService.verify_document(db, current_user, request.document_type_id)