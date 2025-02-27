from pydantic import BaseModel, EmailStr
from datetime import date

# ------------------ Register Schema ------------------
class RegisterSchema(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    dob: date
    gender_id: int
    password: str

# ------------------ Login Schema ------------------
class LoginSchema(BaseModel):
    identifier: str
    password: str

# ------------------ Change Password Schema ------------------
class ChangePasswordSchema(BaseModel):
    identifier: str
    current_password: str
    new_password: str
    confirm_new_password: str

# ------------------ Request Password Reset Schema ------------------
class RequestPasswordResetSchema(BaseModel):
    identifier: str

# ------------------ Reset Password Schema ------------------
class ResetPasswordSchema(BaseModel):
    token: str
    current_password: str
    new_password: str
    confirm_new_password: str

# ------------------ Forgot Password Schema ------------------
class ForgotPasswordSchema(BaseModel):
    email: EmailStr
