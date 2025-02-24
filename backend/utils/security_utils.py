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
    def get_otp_expiry(minutes: int = 10) -> datetime:
        """Get OTP expiry time (10 minutes from now, UTC aware)."""
        return datetime.now(timezone.utc) + timedelta(minutes=minutes)

