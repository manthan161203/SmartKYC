from passlib.context import CryptContext
import jwt
import datetime
from backend.config.config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(email: str, expires_delta: int = 1) -> str:
    token_data = {
        "sub": email,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=expires_delta)
    }
    return jwt.encode(token_data, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
