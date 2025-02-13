from backend.database.model.user_model import User
from backend.database.model.document_model import Document
from backend.database.enums import DocumentStatus, OTPStatus, DocumentType
from backend.database import Base
from sqlalchemy import MetaData

metadata = MetaData()
