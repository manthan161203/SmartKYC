from pydantic import BaseModel

class VerifyOTPSchema(BaseModel):
    user_id: int
    otp_code: str

class UserOTPSchema(BaseModel):
    user_id: int
