import re
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from datetime import date, datetime

# Regular expressions for validation
EMAIL_REGEX = re.compile(r'^\S+@\S+\.\S+$')
PHONE_REGEX = re.compile(r'^\+?\d{10,15}$')

# Utility function for password validation
def validate_password(value: str) -> str:
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

# ------------------ Register Schema ------------------
class RegisterSchema(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name must be between 2 and 100 characters.",
        example="John Doe"
    )
    email: EmailStr = Field(
        ...,
        description="A valid email address.",
        example="john.doe@example.com"
    )
    phone_number: str = Field(
        ...,
        min_length=10,
        max_length=15,
        pattern=r"^\+?\d{10,15}$",
        description="Phone number must be 10 to 15 digits.",
        example="+1234567890"
    )
    dob: date = Field(
        ...,
        description="Date of birth (must be at least 18 years old).",
        example="2000-01-01"
    )
    gender_id: int = Field(
        ...,
        gt=0,
        description="Gender ID must be a positive integer.",
        example=1  # Assuming '1' represents Male in your gender type table
    )
    password: str = Field(
        ...,
        description="Password must meet security standards (at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character).",
        example="StrongP@ssw0rd"
    )

    @field_validator("dob")
    @classmethod
    def validate_age(cls, value: date) -> date:
        today = datetime.today().date()
        age = (today - value).days // 365
        if age < 18:
            raise ValueError("User must be at least 18 years old.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password(value)

# ------------------ Login Schema ------------------
class LoginSchema(BaseModel):
    identifier: str = Field(
        ...,
        description="A valid email address or phone number.",
        example="john.doe@example.com"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.",
        example="StrongP@ssw0rd"
    )

    @field_validator("identifier")
    @classmethod
    def validate_identifier(cls, value: str) -> str:
        """Validate identifier as email or phone number."""
        if EMAIL_REGEX.match(value) or PHONE_REGEX.match(value):
            return value
        raise ValueError("Identifier must be a valid email or phone number.")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password(value)

# ------------------ Change Password Schema ------------------
class ChangePasswordSchema(BaseModel):
    identifier: str = Field(
        ...,
        description="A valid email address or phone number.",
        example="john.doe@example.com"  # Can be email or phone number
    )
    current_password: str = Field(
        ...,
        min_length=8,
        description="Current password (must meet the same security standards as new password).",
        example="CurrentP@ssw0rd"
    )
    new_password: str = Field(
        ...,
        min_length=8,
        description="New password must meet security standards (at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character).",
        example="NewP@ssw0rd"
    )
    confirm_new_password: str = Field(
        ...,
        min_length=8,
        description="Confirm new password (must match the new password).",
        example="NewP@ssw0rd"
    )

    @field_validator("identifier")
    @classmethod
    def validate_identifier(cls, value: str) -> str:
        """Validate identifier as email or phone number."""
        if EMAIL_REGEX.match(value) or PHONE_REGEX.match(value):
            return value
        raise ValueError("Identifier must be a valid email or phone number.")

    @field_validator("current_password")
    @classmethod
    def validate_current_password(cls, value: str) -> str:
        """Ensure the current password meets basic length requirements."""
        if len(value) < 8:
            raise ValueError("Current password must be at least 8 characters long.")
        return value

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        """Ensure the new password meets security standards."""
        return validate_password(value)

    @model_validator(mode="before")
    @classmethod
    def check_new_passwords(cls, values: dict) -> dict:
        """Ensure new password and confirm password match."""
        if values.get("new_password") != values.get("confirm_new_password"):
            raise ValueError("New password and confirmation do not match.")
        return values

# ------------------ Request Password Reset Schema ------------------
class RequestPasswordResetSchema(BaseModel):
    identifier: str = Field(
        ...,
        description="A valid email address or phone number.",
        example="john.doe@example.com"
    )

    @field_validator("identifier")
    @classmethod
    def validate_identifier(cls, value: str) -> str:
        """Validate identifier as email or phone number."""
        if EMAIL_REGEX.match(value) or PHONE_REGEX.match(value):
            return value
        raise ValueError("Identifier must be a valid email or phone number.")

# ------------------ Reset Password Schema ------------------
class ResetPasswordSchema(BaseModel):
    token: str = Field(..., description="Password reset token received via email.")
    current_password: str = Field(
        ..., min_length=8, description="Current password.", example="CurrentP@ssw0rd"
    )
    new_password: str = Field(
        ..., min_length=8, description="New password.", example="NewP@ssw0rd"
    )
    confirm_new_password: str = Field(
        ..., min_length=8, description="Confirm new password.", example="NewP@ssw0rd"
    )

    @model_validator(mode="before")
    @classmethod
    def check_new_passwords(cls, values: dict) -> dict:
        """Ensure new password and confirm password match."""
        if values.get("new_password") != values.get("confirm_new_password"):
            raise ValueError("New password and confirmation do not match.")
        return values