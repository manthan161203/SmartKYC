from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
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

class LoginSchema(BaseModel):
    identifier: str = Field(..., description="A valid email address or phone number")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")

    @field_validator("identifier")
    @classmethod
    def validate_identifier(cls, value: str) -> str:
        # Simple regex for email and phone validation
        email_regex = r'^\S+@\S+\.\S+$'
        phone_regex = r'^\+?\d{10,15}$'
        if re.match(email_regex, value) or re.match(phone_regex, value):
            return value
        raise ValueError("Identifier must be a valid email or phone number.")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value

class ChangePasswordSchema(BaseModel):
    identifier: str = Field(..., description="A valid email address or phone number")
    current_password: str = Field(..., min_length=8, description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_new_password: str = Field(..., min_length=8, description="Confirm new password")

    @model_validator(mode="before")
    @classmethod
    def check_new_passwords(cls, values: dict) -> dict:
        new_pass = values.get("new_password")
        confirm_pass = values.get("confirm_new_password")
        if new_pass != confirm_pass:
            raise ValueError("New password and confirmation do not match.")
        return values

    @field_validator("identifier")
    @classmethod
    def validate_identifier(cls, value: str) -> str:
        email_regex = r'^\S+@\S+\.\S+$'
        phone_regex = r'^\+?\d{10,15}$'
        if re.match(email_regex, value) or re.match(phone_regex, value):
            return value
        raise ValueError("Identifier must be a valid email or phone number.")

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("New password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("New password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("New password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("New password must contain at least one special character.")
        return value

    @field_validator("current_password")
    @classmethod
    def validate_current_password(cls, value: str) -> str:
        # Optionally, you can enforce password rules on current password as well
        if len(value) < 8:
            raise ValueError("Current password must be at least 8 characters long.")
        return value