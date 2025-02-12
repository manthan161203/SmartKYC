import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")