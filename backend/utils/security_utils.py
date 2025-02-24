import random
import string
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """Generate a random OTP with a given length."""
        otp = ''.join(random.choices(string.digits, k=length))
        return otp

    @staticmethod
    def set_otp_expiry() -> datetime:
        """Set OTP expiry time (10 minutes from now)."""
        return datetime.now(tz=timezone.utc) + timedelta(minutes=10)
