from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.config.database import get_db
from backend.services.extract_details_service import ExtractDetailsService
from backend.models.user_model import User
from backend.utils.jwt_middleware import get_current_user

router = APIRouter(prefix="/extract_details", tags=["Extract Details"])

# ✅ Define a request model for the body
class ExtractDetailsRequest(BaseModel):
    document_type_id: int

@router.post("/")
def extract_document_details(
    request: ExtractDetailsRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    API to extract document details using the authenticated user's email.
    """
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return ExtractDetailsService.extract_details(db, user.id, request.document_type_id)