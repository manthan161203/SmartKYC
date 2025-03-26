from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.utils.jwt_middleware import get_current_user
from backend.services.face_verification_service import FaceVerificationService

router = APIRouter(prefix="/verify_kyc", tags=["Face Verification"])

@router.post("/")
def verify_kyc(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    API to verify user KYC by face matching.
    """
    return FaceVerificationService.verify_kyc(current_user, db)