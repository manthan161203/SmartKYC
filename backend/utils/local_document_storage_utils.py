from __future__ import annotations

import os
import uuid
from sqlalchemy.orm import Session

from backend.models.document_model import Document
from backend.models.document_type_model import DocumentType

UPLOAD_ROOT = os.path.abspath("uploaded_files")


def get_document_type_name(db: Session, document_type_id: int) -> str:
    document_type = db.query(DocumentType).filter(DocumentType.id == document_type_id).first()
    return document_type.name if document_type else "other"


def _clear_document_folder(user_id: int, document_type_name: str) -> None:
    folder_path = os.path.join(UPLOAD_ROOT, str(user_id), document_type_name)
    if not os.path.isdir(folder_path):
        return

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def save_document_file(
    db: Session,
    *,
    file_obj,
    original_file_name: str,
    user_id: int,
    document_type_id: int,
) -> str:
    document_type_name = get_document_type_name(db, document_type_id)
    _clear_document_folder(user_id, document_type_name)

    unique_file_name = f"{uuid.uuid4()}_{original_file_name}"
    folder_path = os.path.join(UPLOAD_ROOT, str(user_id), document_type_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, unique_file_name)

    with open(file_path, "wb") as target:
        target.write(file_obj.read())
    return file_path


def get_latest_user_document_path(db: Session, user_id: int, document_type_id: int) -> str:
    document = (
        db.query(Document)
        .filter(Document.user_id == user_id, Document.document_type_id == document_type_id)
        .order_by(Document.updated_at.desc(), Document.id.desc())
        .first()
    )
    if not document:
        raise ValueError("No documents found for the user.")
    return document.file_path
