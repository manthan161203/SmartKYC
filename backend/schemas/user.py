from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str 
    username: str  
    email: str     
    phone: Optional[str] = None
    password: str
    address: Optional[str] = None
    aadhaar_card_number: Optional[str] = None
    pan_card_number: Optional[str] = None

    class Config:
        from_attributes = True
