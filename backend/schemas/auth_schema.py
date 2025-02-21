from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime
import re

class RegisterSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name must be between 2 and 100 characters.")
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15, pattern=r"^\+?\d{10,15}$", description="Phone number must be 10 to 15 digits.")
    dob: date
    gender_id: int = Field(..., gt=0, description="Gender ID must be a positive integer.")
    hashed_password: str

    @field_validator("dob")
    @classmethod
    def validate_age(cls, value: date) -> date:
        """Ensure the user is at least 18 years old."""
        today = datetime.today().date()
        age = (today - value).days // 365
        if age < 18:
            raise ValueError("User must be at least 18 years old.")
        return value

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Ensure password meets security standards."""
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value
