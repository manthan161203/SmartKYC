from pydantic import BaseModel, Field

class VerifyOTPSchema(BaseModel):
    user_id: int = Field(..., example=123, description="User ID for OTP verification")
    otp_code: str = Field(..., min_length=4, max_length=6, example="123456", description="The OTP code")

class UserOTPSchema(BaseModel):
    user_id: int = Field(..., example=123, description="User ID for OTP verification")
