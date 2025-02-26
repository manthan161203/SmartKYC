from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional

class UserAddressSchema(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    country: str
    postal_code: str

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: EmailStr
    dob: datetime
    profile_photo: Optional[str] = None
    is_email_verified: bool
    is_phone_verified: bool
    gender_id: int
    kyc_status_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    addresses: list[UserAddressSchema] = []

    class Config:
        from_attributes = True
