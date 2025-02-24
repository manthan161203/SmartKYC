from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from backend.models.gender_type_model import GenderType
from backend.schemas.profile_schema import GenderTypeResponse

class ProfileService:
    async def get_gender_types(self, db: Session):
        """Fetch all gender types with proper error handling."""
        try:
            genders = db.query(GenderType).all()

            if not genders:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No gender types found."
                )

            # Return the gender types using the GenderTypeResponse schema
            return [GenderTypeResponse(id=gender.id, type=gender.type) for gender in genders]

        except SQLAlchemyError as sae:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error occurred: {str(sae)}"
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )
