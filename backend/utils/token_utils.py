from time import timezone
import jwt
import datetime
from typing import Optional
from backend.config.config import settings
from fastapi import HTTPException, status

class TokenUtils:
    """Utility class for generating and verifying tokens."""

    SECRET_KEY = settings.JWT_SECRET_KEY
    ALGORITHM = settings.JWT_ALGORITHM
    EXPIRATION_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    @staticmethod
    def generate_token(identifier: str, purpose: str, expires_in: Optional[int] = None) -> str:
        """
        Generate a JWT token for authentication or password reset.

        Args:
            identifier (str): The user's unique identifier (email or phone).
            purpose (str): Purpose of the token (e.g., "reset_password", "auth").
            expires_in (int, optional): Custom expiration time in minutes.

        Returns:
            str: Encoded JWT token.
        """
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=expires_in if expires_in else TokenUtils.EXPIRATION_MINUTES
        )

        payload = {
            "sub": identifier,
            "purpose": purpose,
            "exp": expiration_time,
            "iat": datetime.datetime.now(datetime.timezone.utc),
        }

        token = jwt.encode(payload, TokenUtils.SECRET_KEY, algorithm=TokenUtils.ALGORITHM)
        return token

    @staticmethod
    def verify_token(token: str, expected_purpose: str) -> str:
        """
        Verify and decode a JWT token.

        Args:
            token (str): The JWT token to verify.
            expected_purpose (str): Expected purpose of the token.

        Returns:
            str: The identifier (email or phone) if valid.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        try:
            decoded_token = jwt.decode(token, TokenUtils.SECRET_KEY, algorithms=[TokenUtils.ALGORITHM])

            if decoded_token["purpose"] != expected_purpose:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token purpose.",
                )

            return decoded_token["sub"]  # Return identifier

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired.",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
            )