from sqlalchemy import select
from backend.config.database import SessionLocal
from backend.models.gender_type_model import GenderType
from backend.models.kyc_status_model import KYCStatus
from backend.models.otp_status_model import OTPStatus
from backend.models.document_type_model import DocumentType

def seed_reference_tables():
    """
    Seeds fixed reference tables (GenderType, KYCStatus, OTPStatus, DocumentType)
    with initial data if they are empty.
    """
    session = SessionLocal()
    try:
        # Seed GenderType table
        if not session.execute(select(GenderType)).scalars().first():
            genders = [
                GenderType(id=1, type="Male"),
                GenderType(id=2, type="Female"),
                GenderType(id=3, type="Other")
            ]
            session.bulk_save_objects(genders)
        
        # Seed KYCStatus table
        if not session.execute(select(KYCStatus)).scalars().first():
            statuses = [
                KYCStatus(id=1, status="Pending"),
                KYCStatus(id=2, status="Verified"),
                KYCStatus(id=3, status="Rejected")
            ]
            session.bulk_save_objects(statuses)
        
        # Seed OTPStatus table
        if not session.execute(select(OTPStatus)).scalars().first():
            otp_statuses = [
                OTPStatus(id=1, status="Sent"),
                OTPStatus(id=2, status="Not Sent"),
                OTPStatus(id=3, status="Verified")
            ]
            session.bulk_save_objects(otp_statuses)
        
        # Seed DocumentType table
        if not session.execute(select(DocumentType)).scalars().first():
            doc_types = [
                DocumentType(id=1, name="aadhaar_front"),
                DocumentType(id=2, name="aadhaar_back"),
                DocumentType(id=3, name="pan"),
                DocumentType(id=4, name="selfie"),
                DocumentType(id=5, name="profile_photo")
            ]
            session.bulk_save_objects(doc_types)
        
        session.commit()
    finally:
        session.close()
