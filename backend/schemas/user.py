from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str 
    username: str  
    email: str     
    phone: Optional[str] = None
    password: str

    class Config:
        from_attributes = True