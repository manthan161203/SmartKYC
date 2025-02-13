from enum import Enum as PyEnum

class DocumentStatus(PyEnum):
    NOT_VERIFIED = "not_verified"
    VERIFIED = "verified"
    PENDING = "pending"

class OTPStatus(PyEnum):
    SENT = "sent"
    VERIFIED = "verified"
    EXPIRED = "expired"

class DocumentType(PyEnum):
    AADHAAR = "aadhaar"
    PAN = "pan"
    PASSPORT = "passport"
    ELECTION = "election"
