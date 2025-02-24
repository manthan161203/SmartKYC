from pydantic import BaseModel, Field

class GenderTypeResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the gender type", example=1)
    type: str = Field(..., description="The gender type (e.g., 'Male', 'Female', 'Other')", example="Male")
