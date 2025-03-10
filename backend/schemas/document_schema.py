from pydantic import BaseModel
from typing import Optional, Dict

class DocumentUploadRequest(BaseModel):
    user_id: int
    document_type_id: int

class DocumentResponse(BaseModel):
    id: int
    user_id: int
    document_type_id: int
    file_path: str
    is_verified_document: Optional[bool] = False

class DocumentProcessingResponse(BaseModel):
    document_id: int
    extracted_data: Dict
