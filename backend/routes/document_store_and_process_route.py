from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.services.document_store_and_process_service import ProcessAadhaarService
from backend.utils.jwt_middleware import get_current_user

router = APIRouter(prefix="/document_store_and_process", tags=["DocumentStoreAndProcess"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),  
    document_type_id: int = Form(...),  # 🔥 Extract document_type_id from FormData explicitly
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Received document_type_id: {document_type_id} (Type: {type(document_type_id)})")  # Debugging
    response = await ProcessAadhaarService.process_document(db, current_user, file, document_type_id)
    return response