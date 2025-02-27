from pydantic import BaseModel, EmailStr, Field, constr
from datetime import datetime
from typing import Optional, List

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
    addresses: List[UserAddressSchema] = []

    class Config:
        from_attributes = True

class EditUserSchema(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    dob: Optional[datetime] = None
    gender_id: Optional[int] = None
    profile_photo: Optional[str] = None

    # Address fields
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

    class Config:
        from_attributes = True
