import os
from flask import request, jsonify
from backend.database import SessionLocal
from backend.config.config import Config
from backend.database.models import Document

UPLOAD_FOLDER = Config.UPLOAD_FOLDER

@app.route('/upload_documents', methods=['POST'])
def upload_documents():
    db = SessionLocal()
    user_id = request.form['user_id']
    aadhaar = request.files['aadhaar']
    pan = request.files['pan']

    aadhaar_path = os.path.join(UPLOAD_FOLDER, aadhaar.filename)
    pan_path = os.path.join(UPLOAD_FOLDER, pan.filename)

    aadhaar.save(aadhaar_path)
    pan.save(pan_path)

    doc = Document(user_id=user_id, aadhaar_path=aadhaar_path, pan_path=pan_path)
    db.add(doc)
    db.commit()
    db.close()
    
    return jsonify({"message": "Documents uploaded successfully"})