from fastapi import Depends, HTTPException, Security
from backend.services.auth_service import oauth2_scheme
from backend.utils.token_utils import TokenUtils

async def get_current_user(token: str = Security(oauth2_scheme)):
    """
    Extract user identifier from the JWT token.
    """
    try:
        user_email = TokenUtils.verify_token(token, expected_purpose="auth")
        return user_email
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)