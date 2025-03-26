import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.document_model import Document
from backend.models.user_model import User
from backend.utils.face_verification_utils import verify_faces

logger = logging.getLogger(__name__)

class FaceVerificationService:
    @staticmethod
    def verify_kyc(user_email: str, db: Session):
        """
        Verifies KYC by matching the user's Aadhaar (Front) or PAN with their selfie.
        Updates kyc_status_id for both the User and Document models.

        Args:
            user.id (int): ID of the user.
            db (Session): SQLAlchemy session.

        Returns:
            Dict: Verification status and updated KYC status.
        """
        # Get Aadhaar Front, PAN, and Selfie documents

        # Fetch user by email
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        aadhaar_doc = db.query(Document).filter(Document.user_id == user.id, Document.document_type_id == 1).first()
        pan_doc = db.query(Document).filter(Document.user_id == user.id, Document.document_type_id == 3).first()
        selfie_doc = db.query(Document).filter(Document.user_id == user.id, Document.document_type_id == 4).first()

        if not selfie_doc:
            raise HTTPException(status_code=404, detail="Selfie document not found")

        selfie_path = selfie_doc.file_path

        match_found = False  # Flag to check if any document matches

        for doc in [aadhaar_doc, pan_doc]:
            if doc:
                result = verify_faces(doc.file_path, selfie_path)
                if result and result["verified"]:
                    match_found = True
                    break  # No need to check further if one match is found

        # Set KYC status based on the match
        if match_found:
            new_status = 2  # Verified
        elif aadhaar_doc or pan_doc:
            new_status = 3  # Rejected
        else:
            new_status = 1  # Pending

        # # Update KYC status for all documents of the user
        # db.query(Document).filter(Document.user_id == user.id).update({"kyc_status_id": new_status})

        # Update the User's KYC status
        db.query(User).filter(User.id == user.id).update({"kyc_status_id": new_status})

        db.commit()

        status_message = {1: "Pending", 2: "Verified", 3: "Rejected"}[new_status]
        logger.info(f"KYC Status Updated: {status_message} for User {user.id}")

        return {
            "user.id": user.id,
            "kyc_status": new_status,
            "status_message": status_message
        }