import os
import shutil
from sqlalchemy.orm import Session
import logging
from fastapi import UploadFile, HTTPException
from backend.models.user_model import User
from backend.models.document_model import Document
from backend.models.document_type_model import DocumentType
from backend.models.document_details_model import DocumentDetails
from backend.utils.image_processing_ocr import process_image
from backend.utils.openai_utils import build_prompt, query_openai, remove_markdown

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessAadhaarService:
    @staticmethod
    async def process_document(db: Session, email: str, file: UploadFile, document_type_id: int):
        """
        Process an uploaded Aadhaar document based on the document type.
        If a document of the same type already exists for the user, it will be replaced.
        """
        # Validate user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate document type
        doc_type = db.query(DocumentType).filter(DocumentType.id == document_type_id).first()
        if not doc_type:
            raise HTTPException(status_code=404, detail="Document type not found")

        # Define dynamic directory structure
        user_folder = f"uploaded_files/{user.id}"
        doc_folder = f"{user_folder}/{doc_type.name.lower().replace(' ', '_')}"
        os.makedirs(doc_folder, exist_ok=True)  # Ensure the directories exist

        # Check if the user already has a document with the same type
        existing_doc = db.query(Document).filter(
            Document.user_id == user.id,
            Document.document_type_id == document_type_id
        ).first()

        # Validate file extension
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["jpg", "jpeg", "png"]:
            raise HTTPException(status_code=400, detail="Invalid file format")

        file_name = f"{user.id}_{doc_type.name.lower().replace(' ', '_')}.{file_ext}"
        file_path = os.path.join(doc_folder, file_name)

        # If the document already exists, delete the old file
        if existing_doc:
            try:
                if os.path.exists(existing_doc.file_path):
                    os.remove(existing_doc.file_path)  # Delete old file
                    logger.info(f"Old document deleted: {existing_doc.file_path}")
            except Exception as e:
                logger.error(f"Error deleting old file: {str(e)}")

        # Save new file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if document_type_id == 4:  # If it's a selfie, just store the file
            if existing_doc:
                existing_doc.file_path = file_path
                db.commit()
                db.refresh(existing_doc)

                return {
                    "message": "Selfie updated successfully",
                    "document_id": existing_doc.id,
                    "file_path": file_path
                }
            else:
                new_doc = Document(
                    user_id=user.id,
                    document_type_id=doc_type.id,
                    file_path=file_path,
                    is_verified_document=False
                )
                db.add(new_doc)
                db.commit()
                db.refresh(new_doc)

                return {
                    "message": "Selfie uploaded successfully",
                    "document_id": new_doc.id,
                    "file_path": file_path
                }

        # Process image with OCR (for non-selfie documents)
        ocr_json = process_image(file_path)
        prompt = build_prompt(ocr_json, side=doc_type.name.lower())  # Dynamic prompt
        response = query_openai(prompt)
        cleaned_data = remove_markdown(response)

        if existing_doc:
            # Update existing document
            existing_doc.file_path = file_path
            existing_doc.is_verified_document = False  # Reset verification on new upload
            db.commit()
            db.refresh(existing_doc)

            # Update document details
            existing_doc_details = db.query(DocumentDetails).filter(
                DocumentDetails.document_id == existing_doc.id
            ).first()

            if existing_doc_details:
                existing_doc_details.details = cleaned_data  # Update extracted data
            else:
                # If details don't exist, create new
                new_doc_details = DocumentDetails(
                    document_id=existing_doc.id,
                    details=cleaned_data
                )
                db.add(new_doc_details)

            db.commit()
            return {
                "message": f"{doc_type.name} updated successfully",
                "document_id": existing_doc.id,
                "file_path": file_path,
                "extracted_data": cleaned_data
            }

        else:
            # Create new document entry
            new_doc = Document(
                user_id=user.id,
                document_type_id=doc_type.id,
                file_path=file_path,
                is_verified_document=False
            )
            db.add(new_doc)
            db.commit()
            db.refresh(new_doc)

            # Save extracted details
            doc_details = DocumentDetails(
                document_id=new_doc.id,
                details=cleaned_data  # Store cleaned data in JSON format
            )
            db.add(doc_details)
            db.commit()

            return {
                "message": f"{doc_type.name} uploaded successfully",
                "document_id": new_doc.id,
                "file_path": file_path,
                "extracted_data": cleaned_data
            }