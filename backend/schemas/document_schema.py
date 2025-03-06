from pydantic import BaseModel

class DocumentUploadRequest(BaseModel):
    user_id: int
    document_type_id: int

class DocumentResponse(BaseModel):
    id: int
    user_id: int
    document_type_id: int
    file_path: str
    is_verified_document: bool

    class Config:
        from_attributes = True
