from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.user_model import User

class UserService:
    @staticmethod
    async def get_user_by_email(email: str, db: Session):
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
