from pydantic import BaseModel

class GenderTypeResponse(BaseModel):
    id: int
    type: str
