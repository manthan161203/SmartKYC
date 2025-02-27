from pydantic import BaseModel

class VerifyOTPSchema(BaseModel):
    otp_code: str

